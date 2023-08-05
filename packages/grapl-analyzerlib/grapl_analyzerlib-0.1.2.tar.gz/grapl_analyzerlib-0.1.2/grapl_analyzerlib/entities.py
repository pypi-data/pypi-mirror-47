import json
from copy import deepcopy
from typing import Iterator, Tuple
from typing import TypeVar, Optional, List, Dict, Any, Union, Set

from pydgraph import DgraphClient

import grapl_analyzerlib.entity_queries as entity_queries
from grapl_analyzerlib import graph_description_pb2

P = TypeVar("P", bound="ProcessView")
PQ = TypeVar("PQ", bound="ProcessQuery")

F = TypeVar("F", bound="FileView")
FQ = TypeVar("FQ", bound="FileQuery")


N = TypeVar("N", bound="NodeView")

S = TypeVar("S", bound="SubgraphView")


class NodeView(object):
    def __init__(self, node: Union[P, F]):
        self.node = node

    @staticmethod
    def from_raw(dgraph_client: DgraphClient, node: Any) -> N:
        if node.process_node:
            return NodeView(ProcessView(dgraph_client, node.process_node.node_key))
        elif node.file_node:
            return NodeView(FileView(dgraph_client, node.file_node.node_key))
        else:
            raise Exception("Invalid Node Type")

    def as_process_view(self) -> Optional[P]:
        if isinstance(self, ProcessView):
            return self
        return None

    def as_file_view(self) -> Optional[F]:
        if isinstance(self, FileView):
            return self
        return None


class EdgeView(object):
    def __init__(
        self, from_neighbor_key: str, to_neighbor_key: str, edge_name: str
    ) -> None:
        self.from_neighbor_key = from_neighbor_key
        self.to_neighbor_key = to_neighbor_key
        self.edge_name = edge_name


class SubgraphView(object):
    def __init__(
        self, nodes: Dict[str, NodeView], edges: Dict[str, List[EdgeView]]
    ) -> None:
        self.nodes = nodes
        self.edges = edges

    @staticmethod
    def from_proto(dgraph_client: DgraphClient, s: bytes) -> S:
        subgraph = graph_description_pb2.GraphDescription()
        subgraph.ParseFromString(s)

        nodes = {
            k: NodeView.from_raw(dgraph_client, node)
            for k, node in subgraph.nodes.items()
        }
        return SubgraphView(nodes, subgraph.edges)

    def process_iter(self) -> Iterator[P]:
        for node in self.nodes.values():
            maybe_node = node.as_process_view()
            if maybe_node:
                yield maybe_node

    def file_iter(self) -> Iterator[F]:
        for node in self.nodes.values():
            maybe_node = node.as_file_view()
            if maybe_node:
                yield maybe_node


class ProcessQuery(object):
    def __init__(self) -> None:
        # Properties
        self._node_key = None  # type: Optional[entity_queries.Cmp]
        self._process_name = []  # type: List[List[entity_queries.Cmp]]
        self._process_command_line = []  # type: List[List[entity_queries.Cmp]]
        self._process_guid = []  # type: List[List[entity_queries.Cmp]]
        self._process_id = []  # type: List[List[entity_queries.Cmp]]
        self._created_timestamp = []  # type: List[List[entity_queries.Cmp]]
        self._terminated_timestamp = []  # type: List[List[entity_queries.Cmp]]
        self._last_seen_timestamp = []  # type: List[List[entity_queries.Cmp]]

        # Edges
        self._parent = None  # type: Optional[PQ]
        self._bin_file = None  # type: Optional[FQ]
        self._children = None  # type: Optional[PQ]
        self._deleted_files = None  # type: Optional[FQ]
        self._created_files = None  # type: Optional[FQ]
        self._wrote_to_files = None  # type: Optional[FQ]
        self._read_files = None  # type: Optional[FQ]

        # Meta
        self._first = None  # type: Optional[int]

    def with_node_key(self, node_key: Optional[str] = None):
        if node_key:
            self._node_key = entity_queries.Eq("node_key", node_key)
        else:
            self._node_key = entity_queries.Has("node_key")
        return self

    def only_first(self, first: int) -> PQ:
        self._first = first
        return self

    def get_count(self, dgraph_client: DgraphClient):
        query_str = self._to_query(first=True)
        raise NotImplementedError

    def _get_var_block(
        self, binding_num: int, root: Any, already_converted: Set[Any]
    ) -> str:
        if self in already_converted:
            return ""
        already_converted.add(self)

        filters = self._filters()

        parent = entity_queries.get_var_block(
            self._parent, "~children", binding_num, root, already_converted
        )

        children = entity_queries.get_var_block(
            self._children, "children", binding_num, root, already_converted
        )

        deleted_files = entity_queries.get_var_block(
            self._deleted_files, "deleted_files", binding_num, root, already_converted
        )

        block = f"""
            {filters} {{
                {parent}
                {children}
                {deleted_files}
            }}
            """

        return block

    def _get_var_block_root(
        self, binding_num: int, root: Any, node_key: Optional[str] = None
    ) -> str:
        already_converted = {self}
        root_var = ""
        if self == root:
            root_var = f"Binding{binding_num} as "

        filters = self._filters()

        parent = entity_queries.get_var_block(
            self._parent, "~children", binding_num, root, already_converted
        )

        children = entity_queries.get_var_block(
            self._children, "children", binding_num, root, already_converted
        )

        deleted_files = entity_queries.get_var_block(
            self._deleted_files, "deleted_files", binding_num, root, already_converted
        )

        bin_file = entity_queries.get_var_block(
            self._bin_file, "bin_file", binding_num, root, already_converted
        )

        func_filter = """has(process_id)"""
        if node_key:
            func_filter = f'eq(node_key, "{node_key}")'

        block = f"""
            {root_var} var(func: {func_filter}) @cascade {filters} {{
                {parent}
                {children}
                {deleted_files}
                {bin_file}
            }}
            """

        return block

    def get_properties(self) -> List[str]:
        properties = (
            "node_key" if self._node_key else None,
            "process_name" if self._process_name else None,
            "process_command_line" if self._process_command_line else None,
            "process_guid" if self._process_guid else None,
            "process_id" if self._process_id else None,
            "created_timestamp" if self._created_timestamp else None,
            "terminated_timestamp" if self._terminated_timestamp else None,
            "last_seen_timestamp" if self._last_seen_timestamp else None,
        )

        return [p for p in properties if p]

    def get_neighbors(self) -> List[Any]:
        neighbors = (self._parent, self._bin_file, self._children, self._deleted_files)

        return [n for n in neighbors if n]

    def get_edges(self) -> List[Tuple[str, Any]]:
        neighbors = (
            ("parent", self._parent) if self._parent else None,
            ("bin_file", self._bin_file) if self._bin_file else None,
            ("children", self._children) if self._children else None,
            ("deleted_files", self._deleted_files) if self._deleted_files else None,
        )

        return [n for n in neighbors if n]

    def with_process_name(
        self,
        eq: Optional[
            Union[str, List[str], entity_queries.Not, List[entity_queries.Not]]
        ] = None,
        contains: Optional[
            Union[str, List[str], entity_queries.Not, List[entity_queries.Not]]
        ] = None,
        ends_with: Optional[
            Union[str, List[str], entity_queries.Not, List[entity_queries.Not]]
        ] = None,
    ) -> PQ:
        self._process_name.extend(
            entity_queries._str_cmps("process_name", eq, contains, ends_with)
        )
        return self

    def with_process_command_line(
        self,
        eq: Optional[
            Union[str, List[str], entity_queries.Not, List[entity_queries.Not]]
        ] = None,
        contains: Optional[
            Union[str, List[str], entity_queries.Not, List[entity_queries.Not]]
        ] = None,
        ends_with: Optional[
            Union[str, List[str], entity_queries.Not, List[entity_queries.Not]]
        ] = None,
    ) -> PQ:
        self._process_command_line.extend(
            entity_queries._str_cmps("process_command_line", eq, contains, ends_with)
        )
        return self

    def with_process_guid(
        self,
        eq: Optional[
            Union[str, List[str], entity_queries.Not, List[entity_queries.Not]]
        ] = None,
        contains: Optional[
            Union[str, List[str], entity_queries.Not, List[entity_queries.Not]]
        ] = None,
        ends_with: Optional[
            Union[str, List[str], entity_queries.Not, List[entity_queries.Not]]
        ] = None,
    ) -> PQ:
        self._process_guid.extend(
            entity_queries._str_cmps("process_guid", eq, contains, ends_with)
        )
        return self

    def with_process_id(
        self,
        eq: Optional[
            Union[str, List[int], entity_queries.Not, List[entity_queries.Not]]
        ] = None,
        gt: Optional[
            Union[str, List[int], entity_queries.Not, List[entity_queries.Not]]
        ] = None,
        lt: Optional[
            Union[str, List[int], entity_queries.Not, List[entity_queries.Not]]
        ] = None,
    ) -> PQ:
        self._process_id.extend(entity_queries._int_cmps("process_id", eq, gt, lt))
        return self

    def with_created_timestamp(
        self,
        eq: Optional[
            Union[str, List[int], entity_queries.Not, List[entity_queries.Not]]
        ] = None,
        gt: Optional[
            Union[str, List[int], entity_queries.Not, List[entity_queries.Not]]
        ] = None,
        lt: Optional[
            Union[str, List[int], entity_queries.Not, List[entity_queries.Not]]
        ] = None,
    ) -> PQ:
        self._created_timestamp.extend(
            entity_queries._int_cmps("created_timestamp", eq, gt, lt)
        )
        return self

    def with_terminated_timestamp(
        self,
        eq: Optional[
            Union[str, List[int], entity_queries.Not, List[entity_queries.Not]]
        ] = None,
        gt: Optional[
            Union[str, List[int], entity_queries.Not, List[entity_queries.Not]]
        ] = None,
        lt: Optional[
            Union[str, List[int], entity_queries.Not, List[entity_queries.Not]]
        ] = None,
    ) -> PQ:
        self._terminated_timestamp.extend(
            entity_queries._int_cmps("terminated_timestamp", eq, gt, lt)
        )
        return self

    def with_last_seen_timestamp(
        self,
        eq: Optional[
            Union[str, List[int], entity_queries.Not, List[entity_queries.Not]]
        ] = None,
        gt: Optional[
            Union[str, List[int], entity_queries.Not, List[entity_queries.Not]]
        ] = None,
        lt: Optional[
            Union[str, List[int], entity_queries.Not, List[entity_queries.Not]]
        ] = None,
    ) -> PQ:
        self._last_seen_timestamp.extend(
            entity_queries._int_cmps("last_seen_timestamp", eq, gt, lt)
        )
        return self

    def _filters(self) -> str:
        inner_filters = (
            entity_queries._generate_filter(self._process_name),
            entity_queries._generate_filter(self._process_command_line),
            entity_queries._generate_filter(self._process_guid),
            entity_queries._generate_filter(self._process_id),
        )

        inner_filters = [i for i in inner_filters if i]
        if not inner_filters:
            return ""
        return f"@filter({'AND'.join(inner_filters)})"

    def with_parent(self, process: PQ) -> PQ:
        process: PQ = deepcopy(process)
        process._children = self
        self._parent = process
        return self

    def with_bin_file(self, file: FQ) -> PQ:
        file = deepcopy(file)
        file._spawned_from = self
        self._bin_file = file
        return self

    def with_deleted_files(self, file: FQ) -> PQ:
        file = deepcopy(file)
        file._deleter = self
        self._deleted_files = file
        return self

    def with_created_files(self, file: FQ) -> PQ:
        file = deepcopy(file)
        file._creator = self
        self._created_files = file
        return self

    def with_written_files(self, file: FQ) -> PQ:
        file = deepcopy(file)
        file._writers = self
        self._wrote_to_files = file
        return self

    def with_read_files(self, file: FQ) -> PQ:
        file = deepcopy(file)
        file._readers = self
        self._read_files = file
        return self

    def with_children(self, children: PQ) -> PQ:
        children = deepcopy(children)
        children._parent = self
        self._children = children
        return self

    def _to_query(self, count: bool = False, first: Optional[int] = None) -> str:
        var_block = self._get_var_block_root(0, self)

        return entity_queries.build_query(
            self,
            [var_block],
            ["Binding0"],
            count=count,
            first=first
        )

    def query_first(self, dgraph_client, contains_node_key=None) -> Optional[P]:
        if contains_node_key:
            query_str = entity_queries.get_queries(self, node_key=contains_node_key)
        else:
            query_str = self._to_query(first=True)

        raw_views = json.loads(dgraph_client.txn(read_only=True).query(query_str).json)[
            "res"
        ]

        if not raw_views:
            return None

        return ProcessView.from_dict(dgraph_client, raw_views[0])


class ProcessView(NodeView):
    def __init__(
        self,
        dgraph_client: DgraphClient,
        node_key: str,
        uid: Optional[str] = None,
        process_name: Optional[str] = None,
        process_command_line: Optional[str] = None,
        process_guid: Optional[str] = None,
        process_id: Optional[str] = None,
        created_timestamp: Optional[str] = None,
        terminated_timestamp: Optional[str] = None,
        last_seen_timestamp: Optional[str] = None,
        bin_file: Optional[F] = None,
        parent: Optional[P] = None,
        children: Optional[List[P]] = None,
        deleted_files: Optional[List[F]] = None,
    ) -> None:
        super(ProcessView, self).__init__(self)

        self.dgraph_client = dgraph_client  # type: DgraphClient
        self.node_key = node_key  # type: str
        self.uid = uid  # type: Optional[str]
        self.process_command_line = process_command_line
        self.process_guid = process_guid
        self.process_id = process_id
        self.created_timestamp = created_timestamp
        self.terminated_timestamp = terminated_timestamp
        self.last_seen_timestamp = last_seen_timestamp

        self.process_name = process_name  # type: Optional[str]
        self.bin_file = bin_file  # type: Optional[F]
        self.children = children  # type: Optional[List[P]]
        self.parent = parent  # type: Optional[P]
        self.deleted_files = deleted_files  # type: Optional[List[F]]

    @staticmethod
    def from_dict(dgraph_client: DgraphClient, d: Dict[str, Any]) -> P:
        raw_bin_file = d.get("bin_file", None)

        bin_file = None

        if raw_bin_file:
            bin_file = FileView.from_dict(dgraph_client, raw_bin_file[0])

        raw_parent = d.get("~children", None)

        parent = None

        if raw_parent:
            parent = ProcessView.from_dict(dgraph_client, raw_parent[0])

        raw_deleted_files = d.get("deleted_files", None)

        deleted_files = None

        if raw_deleted_files:
            deleted_files = [
                FileView.from_dict(dgraph_client, f) for f in d["deleted_files"]
            ]

        raw_children = d.get("children", None)

        children = None  # type: Optional[List[P]]
        if raw_children:
            children = [
                ProcessView.from_dict(dgraph_client, child) for child in d["children"]
            ]

        return ProcessView(
            dgraph_client=dgraph_client,
            node_key=d["node_key"],
            uid=d.get("uid", None),
            process_name=d.get("process_name"),
            process_command_line=d.get("process_command_line"),
            process_guid=d.get("process_guid"),
            process_id=d.get("process_id"),
            created_timestamp=d.get("created_timestamp"),
            terminated_timestamp=d.get("terminated_timestamp"),
            last_seen_timestamp=d.get("last_seen_timestamp"),
            bin_file=bin_file,
            deleted_files=deleted_files,
            children=children,
            parent=parent,
        )

    def get_process_name(self) -> Optional[str]:
        if self.process_name:
            return self.process_name

        self_process = (
            ProcessQuery()
            .with_node_key(self.node_key)
            .with_process_name()
            .query_first(dgraph_client=self.dgraph_client)
        )

        if not self_process:
            return None

        self.process_name = self_process[0].process_name
        return self.process_name

    def get_parent(self) -> Optional[P]:
        if self.parent:
            return self.parent

        parent = (
            ProcessQuery()
            .with_children(ProcessQuery().with_node_key(self.node_key))
            .query_first(self.dgraph_client)
        )

        if not parent:
            return None

        self.parent = parent
        return self.parent

    def get_uid(self):
        # type: () -> str
        if self.uid:
            return self.uid

        process = (
            ProcessQuery()
            .with_node_key(self.node_key)
            .with_uid()
            .query_first(self.dgraph_client)
        )

        assert process
        self.uid = process.uid
        return process.uid

    def get_bin_file(self) -> Optional[F]:
        if self.bin_file:
            return self.bin_file

        query = (
            ProcessQuery()
            .with_node_key(self.node_key)
            .with_bin_file(FileQuery())
            .to_query()
        )

        res = json.loads(self.dgraph_client.txn(read_only=True).query(query).json)

        bin_file = res["q0"]["bin_file"]
        self.bin_file = FileView.from_dict(self.dgraph_client, bin_file[0])
        return self.bin_file

    def get_deleted_files(self) -> Optional[List[F]]:
        if self.deleted_files:
            return self.deleted_files

        deleted_files = (
            ProcessQuery()
            .with_node_key(self.node_key)
            .with_deleted_files(FileQuery().with_node_key())
            .query()
        )

        if not deleted_files:
            return None

        self.deleted_files = deleted_files[0].deleted_files
        return self.deleted_files


class FileQuery(object):
    def __init__(self) -> None:
        # Attributes
        self._node_key = None  # type: Optional[entity_queries.Cmp]
        self._file_name = []  # type: List[List[entity_queries.Cmp]]
        self._file_path = []  # type: List[List[entity_queries.Cmp]]
        self._file_extension = []  # type: List[List[entity_queries.Cmp]]
        self._file_mime_type = []  # type: List[List[entity_queries.Cmp]]
        self._file_size = []  # type: List[List[entity_queries.Cmp]]
        self._file_version = []  # type: List[List[entity_queries.Cmp]]
        self._file_description = []  # type: List[List[entity_queries.Cmp]]
        self._file_product = []  # type: List[List[entity_queries.Cmp]]
        self._file_company = []  # type: List[List[entity_queries.Cmp]]
        self._file_directory = []  # type: List[List[entity_queries.Cmp]]
        self._file_inode = []  # type: List[List[entity_queries.Cmp]]
        self._file_hard_links = []  # type: List[List[entity_queries.Cmp]]
        self._md5_hash = []  # type: List[List[entity_queries.Cmp]]
        self._sha1_hash = []  # type: List[List[entity_queries.Cmp]]
        self._sha256_hash = []  # type: List[List[entity_queries.Cmp]]

        # Edges
        self._creator = None  # type: Optional[PQ]
        self._deleter = None  # type: Optional[PQ]
        self._writers = None  # type: Optional[PQ]
        self._readers = None  # type: Optional[PQ]
        self._spawned_from = None  # type: Optional[PQ]

    def with_node_key(self, node_key: Optional[str] = None):
        if node_key:
            self._node_key = entity_queries.Eq("node_key", node_key)
        else:
            self._node_key = entity_queries.Has("node_key")
        return self

    def with_file_name(self, eq=None, contains=None, ends_with=None) -> FQ:
        self._file_name.extend(
            entity_queries._str_cmps("file_name", eq, contains, ends_with)
        )
        return self

    def with_file_path(self, eq=None, contains=None, ends_with=None) -> FQ:
        self._file_path.extend(
            entity_queries._str_cmps("file_path", eq, contains, ends_with)
        )
        return self

    def with_file_extension(self, eq=None, contains=None, ends_with=None) -> FQ:
        self._file_extension.extend(
            entity_queries._str_cmps("file_extension", eq, contains, ends_with)
        )
        return self

    def with_file_mime_type(self, eq=None, contains=None, ends_with=None) -> FQ:
        self._file_mime_type.extend(
            entity_queries._str_cmps("file_mime_type", eq, contains, ends_with)
        )
        return self

    def with_file_size(self, eq=None, contains=None, ends_with=None) -> FQ:
        self._file_size.extend(
            entity_queries._str_cmps("file_size", eq, contains, ends_with)
        )
        return self

    def with_file_version(self, eq=None, contains=None, ends_with=None) -> FQ:
        self._file_version.extend(
            entity_queries._str_cmps("file_version", eq, contains, ends_with)
        )
        return self

    def with_file_description(self, eq=None, contains=None, ends_with=None) -> FQ:
        self._file_description.extend(
            entity_queries._str_cmps("file_description", eq, contains, ends_with)
        )
        return self

    def with_file_product(self, eq=None, contains=None, ends_with=None) -> FQ:
        self._file_product.extend(
            entity_queries._str_cmps("file_product", eq, contains, ends_with)
        )
        return self

    def with_file_company(self, eq=None, contains=None, ends_with=None) -> FQ:
        self._file_company.extend(
            entity_queries._str_cmps("file_company", eq, contains, ends_with)
        )
        return self

    def with_file_directory(self, eq=None, contains=None, ends_with=None) -> FQ:
        self._file_directory.extend(
            entity_queries._str_cmps("file_directory", eq, contains, ends_with)
        )
        return self

    def with_file_inode(self, eq=None, contains=None, ends_with=None) -> FQ:
        self._file_inode.extend(
            entity_queries._str_cmps("file_inode", eq, contains, ends_with)
        )
        return self

    def with_file_hard_links(self, eq=None, contains=None, ends_with=None) -> FQ:
        self._file_hard_links.extend(
            entity_queries._str_cmps("file_hard_links", eq, contains, ends_with)
        )
        return self

    def with_md5_hash(self, eq=None, contains=None, ends_with=None) -> FQ:
        self._md5_hash.extend(
            entity_queries._str_cmps("md5_hash", eq, contains, ends_with)
        )
        return self

    def with_sha1_hash(self, eq=None, contains=None, ends_with=None) -> FQ:
        self._sha1_hash.extend(
            entity_queries._str_cmps("sha1_hash", eq, contains, ends_with)
        )
        return self

    def with_sha256_hash(self, eq=None, contains=None, ends_with=None) -> FQ:
        self._sha256_hash.extend(
            entity_queries._str_cmps("sha256_hash", eq, contains, ends_with)
        )
        return self

    def with_creator(self, creator: PQ) -> FQ:
        creator = deepcopy(creator)
        self._creator = creator
        return self

    def with_deleter(self, deleter: PQ) -> FQ:
        deleter = deepcopy(deleter)
        self._deleter = deleter
        deleter._deleted_files = self
        return self

    def with_writers(self, writers: PQ) -> FQ:
        writers = deepcopy(writers)
        self._writers = writers
        return self

    def with_readers(self, readers: PQ) -> FQ:
        readers = deepcopy(readers)
        self._readers = readers
        readers._read_files = self
        return self

    def _get_var_block(self, binding_num, root, already_converted) -> str:
        if self in already_converted:
            return ""
        already_converted.add(self)

        filters = self._filters()

        creator = entity_queries.get_var_block(
            self._creator, "~created_files", binding_num, root, already_converted
        )

        deleter = entity_queries.get_var_block(
            self._deleter, "~deleted_files", binding_num, root, already_converted
        )

        writers = entity_queries.get_var_block(
            self._writers, "~wrote_files", binding_num, root, already_converted
        )

        readers = entity_queries.get_var_block(
            self._readers, "~read_files", binding_num, root, already_converted
        )

        block = f"""
            {filters} {{
                {creator}
                {deleter}
                {writers}
                {readers}
            }}
            """

        return block

    def _get_var_block_root(
        self, binding_num: int, root: Any, node_key: Optional[str] = None
    ):
        already_converted = {self}
        root_var = ""
        if self == root:
            root_var = f"Binding{binding_num} as "

        filters = self._filters()

        creator = entity_queries.get_var_block(
            self._creator, "~created_files", binding_num, root, already_converted
        )

        deleter = entity_queries.get_var_block(
            self._deleter, "~deleted_files", binding_num, root, already_converted
        )

        writers = entity_queries.get_var_block(
            self._writers, "~wrote_files", binding_num, root, already_converted
        )

        readers = entity_queries.get_var_block(
            self._readers, "~read_files", binding_num, root, already_converted
        )

        spawned_from = entity_queries.get_var_block(
            self._spawned_from, "~bin_file", binding_num, root, already_converted
        )

        func_filter = """has(file_path)"""
        if node_key:
            func_filter = f'eq(node_key, "{node_key}")'

        block = f"""
            {root_var} var(func: {func_filter}) @cascade {filters} {{
                {creator}
                {deleter}
                {writers}
                {readers}
                {spawned_from}
            }}
            """

        return block

    def _filters(self) -> str:
        inner_filters = (
            entity_queries._generate_filter(self._file_name),
            entity_queries._generate_filter(self._file_path),
            entity_queries._generate_filter(self._file_extension),
            entity_queries._generate_filter(self._file_mime_type),
            entity_queries._generate_filter(self._file_size),
            entity_queries._generate_filter(self._file_version),
            entity_queries._generate_filter(self._file_description),
            entity_queries._generate_filter(self._file_product),
            entity_queries._generate_filter(self._file_company),
            entity_queries._generate_filter(self._file_directory),
            entity_queries._generate_filter(self._file_inode),
            entity_queries._generate_filter(self._file_hard_links),
            entity_queries._generate_filter(self._md5_hash),
            entity_queries._generate_filter(self._sha1_hash),
            entity_queries._generate_filter(self._sha256_hash),
        )

        inner_filters = [i for i in inner_filters if i]
        if not inner_filters:
            return ""

        return f"@filter({'AND'.join(inner_filters)})"

    def get_neighbors(self) -> List[Any]:
        neighbors = (
            self._creator,
            self._deleter,
            self._writers,
            self._readers,
            self._spawned_from,
        )

        return [n for n in neighbors if n]


class FileView(NodeView):
    def __init__(
        self,
        dgraph_client: DgraphClient,
        node_key: str,
        uid: Optional[str] = None,
        file_name: Optional[str] = None,
        file_path: Optional[str] = None,
        file_extension: Optional[str] = None,
        file_mime_type: Optional[str] = None,
        file_size: Optional[int] = None,
        file_version: Optional[str] = None,
        file_description: Optional[str] = None,
        file_product: Optional[str] = None,
        file_company: Optional[str] = None,
        file_directory: Optional[str] = None,
        file_inode: Optional[str] = None,
        file_hard_links: Optional[int] = None,
        md5_hash: Optional[str] = None,
        sha1_hash: Optional[str] = None,
        sha256_hash: Optional[str] = None,
    ) -> None:
        super(FileView, self).__init__(self)
        self.dgraph_client = dgraph_client  # type: DgraphClient
        self.node_key = node_key  # type: Optional[str]
        self.uid = uid  # type: Optional[str]
        self.file_name = file_name
        self.file_path = file_path
        self.file_extension = file_extension
        self.file_mime_type = file_mime_type
        self.file_size = int(file_size)
        self.file_version = file_version
        self.file_description = file_description
        self.file_product = file_product
        self.file_company = file_company
        self.file_directory = file_directory
        self.file_inode = int(file_inode)
        self.file_hard_links = file_hard_links
        self.md5_hash = md5_hash
        self.sha1_hash = sha1_hash
        self.sha256_hash = sha256_hash

    @staticmethod
    def from_dict(dgraph_client: DgraphClient, d: Dict[str, Any]) -> F:
        return FileView(
            dgraph_client=dgraph_client,
            node_key=d["node_key"],
            uid=d.get("uid"),
            file_name=d.get("file_name"),
            file_path=d.get("file_path"),
            file_extension=d.get("file_extension"),
            file_mime_type=d.get("file_mime_type"),
            file_size=d.get("file_size"),
            file_version=d.get("file_version"),
            file_description=d.get("file_description"),
            file_product=d.get("file_product"),
            file_company=d.get("file_company"),
            file_directory=d.get("file_directory"),
            file_inode=d.get("file_inode"),
            file_hard_links=d.get("file_hard_links"),
            md5_hash=d.get("md5_hash"),
            sha1_hash=d.get("sha1_hash"),
            sha256_hash=d.get("sha256_hash"),
        )


"""


{
    Binding0 as var(func: eq(node_key, "keyA")) @cascade 
        @filter(( (NOT regexp(process_name, /.*services\.exe.*/i)) )) 
        {
            children { } 
        }
    
    var(func: eq(node_key, "keyA")) @cascade {
        Binding1 as ~children
        @filter(( (NOT regexp(process_name, /.*services\.exe.*/i)) ))
        {
        }
    }
            
    res(func: uid(Binding0, Binding1), first: 1) {
        expand(_all_) {
            expand(_all_) {
                expand(_all_)
            }
        }
    }    
}

"""
