# -*- coding: utf-8 -*-
# ptrie.py
# Copyright (c) 2013-2019 Pablo Acosta-Serafini
# See LICENSE for details
# pylint: disable=C0111,R0205,R0913,W0105,W0212

# Standard library imports
import copy
import sys


###
# Classes
###
class Trie(object):
    r"""
    Provides basic `trie <https://en.wikipedia.org/wiki/Trie>`_ functionality.

    :param node_separator: Single character used to separate nodes in the tree
    :type  node_separator: string

    :rtype: :py:class:`ptrie.Trie` object

    :raises: RuntimeError (Argument \`node_separator\` is not valid)
    """

    # pylint: disable=E0602,R0902,R0903
    def __init__(self, node_separator="."):  # noqa
        self._db = {}
        self._root = None
        self._root_hierarchy_length = None
        ufunc = unichr if sys.hexversion < 0x03000000 else chr
        # Characters from http://www.unicode.org/charts/PDF/U2500.pdf
        self._vertical = ufunc(0x2502)
        self._vertical_and_right = ufunc(0x251C)
        self._up_and_right = ufunc(0x2514)
        if (not isinstance(node_separator, str)) or (
            isinstance(node_separator, str) and len(node_separator) != 1
        ):
            raise RuntimeError("Argument `node_separator` is not valid")
        self._node_separator = node_separator

    def __bool__(self):  # pragma: no cover
        """
        Return :code:`False` if tree object has no nodes, :code:`True` otherwise.

        For example:

            >>> from __future__ import print_function
            >>> import ptrie
            >>> tobj = ptrie.Trie()
            >>> if tobj:
            ...     print('Boolean test returned: True')
            ... else:
            ...     print('Boolean test returned: False')
            Boolean test returned: False
            >>> tobj.add_nodes([{'name':'root.branch1', 'data':5}])
            >>> if tobj:
            ...     print('Boolean test returned: True')
            ... else:
            ...     print('Boolean test returned: False')
            Boolean test returned: True
        """
        return bool(self._db)

    def __eq__(self, other):  # noqa
        """
        Test object equality.

        For example:

            >>> from __future__ import print_function
            >>> import copy
            >>> import ptrie
            >>> tobj1 = ptrie.Trie()
            >>> tobj1.add_nodes([
            ...     {'name':'root.branch1', 'data':5},
            ...     {'name':'root.branch2', 'data':[]},
            ...     {'name':'root.branch1.leaf1', 'data':[]},
            ...     {'name':'root.branch1.leaf2', 'data':'Hello world!'}
            ... ])
            >>> print(tobj1)
            root
            ├branch1 (*)
            │├leaf1
            │└leaf2 (*)
            └branch2
            >>> tobj2 = copy.copy(tobj1)
            >>> tobj1 == tobj2
            True
            >>> tobj2.add_nodes({'name':'root.branch1.leaf3', 'data':"xyz"})
            >>> print(tobj2)
            root
            ├branch1 (*)
            │├leaf1
            │├leaf2 (*)
            │└leaf3 (*)
            └branch2
            >>> tobj1 == tobj2
            False
        """
        return (
            isinstance(other, Trie)
            and (self._db == other._db)
            and (self._root == other._root)
            and (self._root_hierarchy_length == other._root_hierarchy_length)
            and (self._node_separator == self._node_separator)
        )

    def __copy__(self, memodict=None):  # noqa
        memodict = {} if memodict is None else memodict
        cobj = Trie(self.node_separator)
        cobj._db = copy.deepcopy(self._db, memodict)
        cobj._root = self._root
        cobj._root_hierarchy_length = self._root_hierarchy_length
        return cobj

    def __nonzero__(self):  # pragma: no cover
        """
        Return :code:`False` if tree object has no nodes, :code:`True` otherwise.

        For example:

            >>> from __future__ import print_function
            >>> import ptrie
            >>> tobj = ptrie.Trie()
            >>> if tobj:
            ...     print('Boolean test returned: True')
            ... else:
            ...     print('Boolean test returned: False')
            Boolean test returned: False
            >>> tobj.add_nodes([{'name':'root.branch1', 'data':5}])
            >>> if tobj:
            ...     print('Boolean test returned: True')
            ... else:
            ...     print('Boolean test returned: False')
            Boolean test returned: True
        """
        return bool(self._db)

    def __str__(self):  # noqa: D302
        """
        Return a string with the tree 'pretty printed' as a character-based structure.

        Only node names are shown, nodes with data are marked with an asterisk
        (:code:`*`).  For example:

            >>> from __future__ import print_function
            >>> import ptrie
            >>> tobj = ptrie.Trie()
            >>> tobj.add_nodes([
            ...     {'name':'root.branch1', 'data':5},
            ...     {'name':'root.branch2', 'data':[]},
            ...     {'name':'root.branch1.leaf1', 'data':[]},
            ...     {'name':'root.branch1.leaf2', 'data':'Hello world!'}
            ... ])
            >>> print(tobj)
            root
            ├branch1 (*)
            │├leaf1
            │└leaf2 (*)
            └branch2

        :rtype: Unicode string
        """
        ret = ""
        if self._db:
            ret = self._prt(name=self.root_name, lparent=-1, sep="", pre1="", pre2="")
        return ret.encode("utf-8") if sys.hexversion < 0x03000000 else ret

    def _collapse_subtree(self, name, recursive=True):
        """Collapse a sub-tree."""
        oname = name
        children = self._db[name]["children"]
        data = self._db[name]["data"]
        del_list = []
        while (len(children) == 1) and (not data):
            del_list.append(name)
            name = children[0]
            children = self._db[name]["children"]
            data = self._db[name]["data"]
        parent = self._db[oname]["parent"]
        self._db[name]["parent"] = parent
        if parent:
            self._db[parent]["children"].remove(oname)
            self._db[parent]["children"] = sorted(self._db[parent]["children"] + [name])
        else:
            self._root = name
            self._root_hierarchy_length = len(
                self.root_name.split(self._node_separator)
            )
        for node in del_list:
            self._del_node(node)
        if recursive:
            for child in copy.copy(children):
                self._collapse_subtree(child)

    def _create_intermediate_nodes(self, name):
        """Create intermediate nodes if hierarchy does not exist."""
        hierarchy = self._split_node_name(name, self.root_name)
        node_tree = [
            self.root_name
            + self._node_separator
            + self._node_separator.join(hierarchy[: num + 1])
            for num in range(len(hierarchy))
        ]
        iobj = [
            (child[: child.rfind(self._node_separator)], child)
            for child in node_tree
            if child not in self._db
        ]
        for parent, child in iobj:
            self._db[child] = {"parent": parent, "children": [], "data": []}
            self._db[parent]["children"] = sorted(
                self._db[parent]["children"] + [child]
            )

    def _create_node(self, name, parent, children, data):
        """Create new tree node."""
        self._db[name] = {"parent": parent, "children": children, "data": data}

    def _delete_prefix(self, name):
        lname = len(name) + 1
        self._root = self._root[lname:]
        self._root_hierarchy_length = len(self.root_name.split(self._node_separator))
        for key, value in list(self._db.items()):
            value["parent"] = (
                value["parent"][lname:] if value["parent"] else value["parent"]
            )
            value["children"] = [child[lname:] for child in value["children"]]
            del self._db[key]
            self._db[key[lname:]] = value

    def _delete_subtree(self, nodes):
        """
        Delete subtree private method.

        No argument validation and usage of getter/setter private methods is
        used for speed
        """
        nodes = nodes if isinstance(nodes, list) else [nodes]
        iobj = [
            (self._db[node]["parent"], node)
            for node in nodes
            if self._node_name_in_tree(node)
        ]
        for parent, node in iobj:
            # Delete link to parent (if not root node)
            del_list = self._get_subtree(node)
            if parent:
                self._db[parent]["children"].remove(node)
            # Delete children (sub-tree)
            for child in del_list:
                del self._db[child]
            if self._empty_tree():
                self._root = None
                self._root_hierarchy_length = None

    def _del_node(self, name):
        """Delete tree node."""
        del self._db[name]

    def _empty_tree(self):
        """Test whether the object (tree) has any nodes/data."""
        return not self._db

    def _find_common_prefix(self, node1, node2):
        """Find common prefix between two nodes."""
        tokens1 = [item.strip() for item in node1.split(self.node_separator)]
        tokens2 = [item.strip() for item in node2.split(self.node_separator)]
        ret = []
        for token1, token2 in zip(tokens1, tokens2):
            if token1 == token2:
                ret.append(token1)
            else:
                break
        return self.node_separator.join(ret)

    def _get_children(self, name):
        return self._db[name]["children"]

    def _get_data(self, name):
        return self._db[name]["data"]

    def _get_nodes(self):
        return None if not self._db else sorted(self._db.keys())

    def _get_node_separator(self):
        return self._node_separator

    def _get_root_name(self):
        return self._root

    def _get_root_node(self):
        return None if not self.root_name else self._db[self.root_name]

    def _get_subtree(self, name):
        return [name] + [
            node
            for child in self._db[name]["children"]
            for node in self._get_subtree(child)
        ]

    def _get_parent(self, name):
        return self._db[name]["parent"]

    def _node_in_tree(self, name):
        if name not in self._db:
            raise RuntimeError("Node {0} not in tree".format(name))
        return True

    def _node_name_in_tree(self, name):
        if name not in self._db:
            raise RuntimeError("Node {0} not in tree".format(name))
        return True

    def _prt(self, name, lparent, sep, pre1, pre2):
        """
        Print a row (leaf) of tree.

        :param name: Full node name
        :type  name: string

        :param lparent: Position in full node name of last separator before
                        node to be printed
        :type  lparent: integer

        :param pre1: Connector next to node name, either a null character if
                     the node to print is the root node, a right angle if node
                     name to be printed is a leaf or a rotated "T" if the node
                     name to be printed is one of many children
        :type  pre1: string
        """
        # pylint: disable=R0914
        nname = name[lparent + 1 :]
        children = self._db[name]["children"]
        ncmu = len(children) - 1
        plst1 = ncmu * [self._vertical_and_right] + [self._up_and_right]
        plst2 = ncmu * [self._vertical] + [" "]
        slist = (ncmu + 1) * [sep + pre2]
        dmark = " (*)" if self._db[name]["data"] else ""
        return "\n".join(
            [
                u"{sep}{connector}{name}{dmark}".format(
                    sep=sep, connector=pre1, name=nname, dmark=dmark
                )
            ]
            + [
                self._prt(child, len(name), sep=schar, pre1=p1, pre2=p2)
                for child, p1, p2, schar in zip(children, plst1, plst2, slist)
            ]
        )

    def _rename_node(self, name, new_name):
        """
        Rename node private method.

        No argument validation and usage of getter/setter private methods is
        used for speed
        """
        # Update parent
        if not self.is_root(name):
            parent = self._db[name]["parent"]
            self._db[parent]["children"].remove(name)
            self._db[parent]["children"] = sorted(
                self._db[parent]["children"] + [new_name]
            )
        # Update children
        iobj = self._get_subtree(name) if name != self.root_name else self.nodes
        for key in iobj:
            new_key = key.replace(name, new_name, 1)
            new_parent = (
                self._db[key]["parent"]
                if key == name
                else self._db[key]["parent"].replace(name, new_name, 1)
            )
            self._db[new_key] = {
                "parent": new_parent,
                "children": [
                    child.replace(name, new_name, 1)
                    for child in self._db[key]["children"]
                ],
                "data": copy.deepcopy(self._db[key]["data"]),
            }
            del self._db[key]
        if name == self.root_name:
            self._root = new_name
            self._root_hierarchy_length = len(
                self.root_name.split(self._node_separator)
            )

    def _search_tree(self, name):
        """Search_tree for nodes that contain a specific hierarchy name."""
        tpl1 = "{sep}{name}{sep}".format(sep=self._node_separator, name=name)
        tpl2 = "{sep}{name}".format(sep=self._node_separator, name=name)
        tpl3 = "{name}{sep}".format(sep=self._node_separator, name=name)
        return sorted(
            [
                node
                for node in self._db
                if (tpl1 in node)
                or node.endswith(tpl2)
                or node.startswith(tpl3)
                or (name == node)
            ]
        )

    def _set_children(self, name, children):
        self._db[name]["children"] = sorted(list(set(children)))

    def _set_data(self, name, data):
        self._db[name]["data"] = data

    def _set_root_name(self, name):
        self._root = name

    def _set_parent(self, name, parent):
        self._db[name]["parent"] = parent

    def _split_node_name(self, name, root_name=None):
        return [
            element.strip() for element in name.strip().split(self._node_separator)
        ][0 if not root_name else self._root_hierarchy_length :]

    def _validate_node_name(self, var_value):
        """Validate NodeName pseudo-type."""
        # pylint: disable=R0201
        var_values = var_value if isinstance(var_value, list) else [var_value]
        for item in var_values:
            if (not isinstance(item, str)) or (
                isinstance(item, str)
                and (
                    (" " in item)
                    or any(
                        [
                            element.strip() == ""
                            for element in item.strip().split(self._node_separator)
                        ]
                    )
                )
            ):
                return True
        return False

    def _validate_nodes_with_data(self, names):
        """Validate NodeWithData pseudo-type."""
        names = names if isinstance(names, list) else [names]
        if not names:
            raise RuntimeError("Argument `nodes` is not valid")
        for ndict in names:
            if (not isinstance(ndict, dict)) or (
                isinstance(ndict, dict) and (set(ndict.keys()) != set(["name", "data"]))
            ):
                raise RuntimeError("Argument `nodes` is not valid")
            name = ndict["name"]
            if (not isinstance(name, str)) or (
                isinstance(name, str)
                and (
                    (" " in name)
                    or any(
                        [
                            element.strip() == ""
                            for element in name.strip().split(self._node_separator)
                        ]
                    )
                )
            ):
                raise RuntimeError("Argument `nodes` is not valid")

    def add_nodes(self, nodes):  # noqa: D302
        r"""
        Add nodes to tree.

        :param nodes: Node(s) to add with associated data. If there are
                      several list items in the argument with the same node
                      name the resulting node data is a list with items
                      corresponding to the data of each entry in the argument
                      with the same node name, in their order of appearance,
                      in addition to any existing node data if the node is
                      already present in the tree
        :type  nodes: :ref:`NodesWithData`

        :raises:
         * RuntimeError (Argument \`nodes\` is not valid)

         * ValueError (Illegal node name: *[node_name]*)

        For example:

        .. =[=cog
        .. import docs.support.incfile
        .. docs.support.incfile.incfile('ptrie_example.py', cog.out)
        .. =]=
        .. code-block:: python

            # ptrie_example.py
            import ptrie

            def create_tree():
                tobj = ptrie.Trie()
                tobj.add_nodes([
                    {'name':'root.branch1', 'data':5},
                    {'name':'root.branch1', 'data':7},
                    {'name':'root.branch2', 'data':[]},
                    {'name':'root.branch1.leaf1', 'data':[]},
                    {'name':'root.branch1.leaf1.subleaf1', 'data':333},
                    {'name':'root.branch1.leaf2', 'data':'Hello world!'},
                    {'name':'root.branch1.leaf2.subleaf2', 'data':[]},
                ])
                return tobj

        .. =[=end=]=

        .. code-block:: python

            >>> from __future__ import print_function
            >>> import docs.support.ptrie_example
            >>> tobj = docs.support.ptrie_example.create_tree()
            >>> print(tobj)
            root
            ├branch1 (*)
            │├leaf1
            ││└subleaf1 (*)
            │└leaf2 (*)
            │ └subleaf2
            └branch2

            >>> tobj.get_data('root.branch1')
            [5, 7]
        """
        self._validate_nodes_with_data(nodes)
        nodes = nodes if isinstance(nodes, list) else [nodes]
        # Create root node (if needed)
        if not self.root_name:
            self._set_root_name(nodes[0]["name"].split(self._node_separator)[0].strip())
            self._root_hierarchy_length = len(
                self.root_name.split(self._node_separator)
            )
            self._create_node(name=self.root_name, parent="", children=[], data=[])
        # Process new data
        for node_dict in nodes:
            name, data = node_dict["name"], node_dict["data"]
            if name not in self._db:
                # Validate node name (root of new node same as tree root)
                if not name.startswith(self.root_name + self._node_separator):
                    raise ValueError("Illegal node name: {0}".format(name))
                self._create_intermediate_nodes(name)
            self._db[name]["data"] += copy.deepcopy(
                data
                if isinstance(data, list) and data
                else ([] if isinstance(data, list) else [data])
            )

    def collapse_subtree(self, name, recursive=True):  # noqa: D302
        r"""
        Collapse a sub-tree.

        Nodes that have a single child and no data are combined with their
        child as a single tree node

        :param name: Root of the sub-tree to collapse
        :type  name: :ref:`NodeName`

        :param recursive: Flag that indicates whether the collapse operation
                          is performed on the whole sub-tree (True) or whether
                          it stops upon reaching the first node where the
                          collapsing condition is not satisfied (False)
        :type  recursive: boolean

        :raises:
         * RuntimeError (Argument \`name\` is not valid)

         * RuntimeError (Argument \`recursive\` is not valid)

         * RuntimeError (Node *[name]* not in tree)

        Using the same example tree created in
        :py:meth:`ptrie.Trie.add_nodes`::

            >>> from __future__ import print_function
            >>> import docs.support.ptrie_example
            >>> tobj = docs.support.ptrie_example.create_tree()
            >>> print(tobj)
            root
            ├branch1 (*)
            │├leaf1
            ││└subleaf1 (*)
            │└leaf2 (*)
            │ └subleaf2
            └branch2
            >>> tobj.collapse_subtree('root.branch1')
            >>> print(tobj)
            root
            ├branch1 (*)
            │├leaf1.subleaf1 (*)
            │└leaf2 (*)
            │ └subleaf2
            └branch2

        ``root.branch1.leaf1`` is collapsed because it only has one child
        (``root.branch1.leaf1.subleaf1``) and no data; ``root.branch1.leaf2``
        is not collapsed because although it has one child
        (``root.branch1.leaf2.subleaf2``) and this child does have data
        associated with it, :code:`'Hello world!'`
        """
        if self._validate_node_name(name):
            raise RuntimeError("Argument `name` is not valid")
        if not isinstance(recursive, bool):
            raise RuntimeError("Argument `recursive` is not valid")
        self._node_in_tree(name)
        self._collapse_subtree(name, recursive)

    def copy_subtree(self, source_node, dest_node):  # noqa: D302
        r"""
        Copy a sub-tree from one sub-node to another.

        Data is added if some nodes of the source sub-tree exist in the
        destination sub-tree

        :param source_name: Root node of the sub-tree to copy from
        :type  source_name: :ref:`NodeName`

        :param dest_name: Root node of the sub-tree to copy to
        :type  dest_name: :ref:`NodeName`

        :raises:
         * RuntimeError (Argument \`dest_node\` is not valid)

         * RuntimeError (Argument \`source_node\` is not valid)

         * RuntimeError (Illegal root in destination node)

         * RuntimeError (Node *[source_node]* not in tree)

        Using the same example tree created in
        :py:meth:`ptrie.Trie.add_nodes`::

            >>> from __future__ import print_function
            >>> import docs.support.ptrie_example
            >>> tobj = docs.support.ptrie_example.create_tree()
            >>> print(tobj)
            root
            ├branch1 (*)
            │├leaf1
            ││└subleaf1 (*)
            │└leaf2 (*)
            │ └subleaf2
            └branch2
            >>> tobj.copy_subtree('root.branch1', 'root.branch3')
            >>> print(tobj)
            root
            ├branch1 (*)
            │├leaf1
            ││└subleaf1 (*)
            │└leaf2 (*)
            │ └subleaf2
            ├branch2
            └branch3 (*)
             ├leaf1
             │└subleaf1 (*)
             └leaf2 (*)
              └subleaf2
        """
        if self._validate_node_name(source_node):
            raise RuntimeError("Argument `source_node` is not valid")
        if self._validate_node_name(dest_node):
            raise RuntimeError("Argument `dest_node` is not valid")
        if source_node not in self._db:
            raise RuntimeError("Node {0} not in tree".format(source_node))
        if not dest_node.startswith(self.root_name + self._node_separator):
            raise RuntimeError("Illegal root in destination node")
        for node in self._get_subtree(source_node):
            self._db[node.replace(source_node, dest_node, 1)] = {
                "parent": self._db[node]["parent"].replace(source_node, dest_node, 1),
                "children": [
                    child.replace(source_node, dest_node, 1)
                    for child in self._db[node]["children"]
                ],
                "data": copy.deepcopy(self._db[node]["data"]),
            }
        self._create_intermediate_nodes(dest_node)
        parent = self._node_separator.join(dest_node.split(self._node_separator)[:-1])
        self._db[dest_node]["parent"] = parent
        self._db[parent]["children"] = sorted(
            self._db[parent]["children"] + [dest_node]
        )

    def delete_prefix(self, name):  # noqa: D302
        r"""
        Delete hierarchy levels from all nodes in the tree.

        :param nodes: Prefix to delete
        :type  nodes: :ref:`NodeName`

        :raises:
         * RuntimeError (Argument \`name\` is not a valid prefix)

         * RuntimeError (Argument \`name\` is not valid)

        For example:

            >>> from __future__ import print_function
            >>> import ptrie
            >>> tobj = ptrie.Trie('/')
            >>> tobj.add_nodes([
            ...     {'name':'hello/world/root', 'data':[]},
            ...     {'name':'hello/world/root/anode', 'data':7},
            ...     {'name':'hello/world/root/bnode', 'data':8},
            ...     {'name':'hello/world/root/cnode', 'data':False},
            ...     {'name':'hello/world/root/bnode/anode', 'data':['a', 'b']},
            ...     {'name':'hello/world/root/cnode/anode/leaf', 'data':True}
            ... ])
            >>> tobj.collapse_subtree('hello', recursive=False)
            >>> print(tobj)
            hello/world/root
            ├anode (*)
            ├bnode (*)
            │└anode (*)
            └cnode (*)
             └anode
              └leaf (*)
            >>> tobj.delete_prefix('hello/world')
            >>> print(tobj)
            root
            ├anode (*)
            ├bnode (*)
            │└anode (*)
            └cnode (*)
             └anode
              └leaf (*)
        """
        if self._validate_node_name(name):
            raise RuntimeError("Argument `name` is not valid")
        if (not self.root_name.startswith(name)) or (self.root_name == name):
            raise RuntimeError("Argument `name` is not a valid prefix")
        self._delete_prefix(name)

    def delete_subtree(self, nodes):  # noqa: D302
        r"""
        Delete nodes (and their sub-trees) from the tree.

        :param nodes: Node(s) to delete
        :type  nodes: :ref:`NodeName` or list of :ref:`NodeName`

        :raises:
         * RuntimeError (Argument \`nodes\` is not valid)

         * RuntimeError (Node *[node_name]* not in tree)

        Using the same example tree created in
        :py:meth:`ptrie.Trie.add_nodes`::

            >>> from __future__ import print_function
            >>> import docs.support.ptrie_example
            >>> tobj = docs.support.ptrie_example.create_tree()
            >>> print(tobj)
            root
            ├branch1 (*)
            │├leaf1
            ││└subleaf1 (*)
            │└leaf2 (*)
            │ └subleaf2
            └branch2
            >>> tobj.delete_subtree(['root.branch1.leaf1', 'root.branch2'])
            >>> print(tobj)
            root
            └branch1 (*)
             └leaf2 (*)
              └subleaf2
        """
        if self._validate_node_name(nodes):
            raise RuntimeError("Argument `nodes` is not valid")
        self._delete_subtree(nodes)

    def flatten_subtree(self, name):  # noqa: D302
        r"""
        Flatten sub-tree.

        Nodes that have children and no data are merged with each child

        :param name: Ending hierarchy node whose sub-trees are to be
                     flattened
        :type  name: :ref:`NodeName`

        :raises:
         * RuntimeError (Argument \`name\` is not valid)

         * RuntimeError (Node *[name]* not in tree)

        Using the same example tree created in
        :py:meth:`ptrie.Trie.add_nodes`::

            >>> from __future__ import print_function
            >>> import docs.support.ptrie_example
            >>> tobj = docs.support.ptrie_example.create_tree()
            >>> tobj.add_nodes([
            ...     {'name':'root.branch1.leaf1.subleaf2', 'data':[]},
            ...     {'name':'root.branch2.leaf1', 'data':'loren ipsum'},
            ...     {'name':'root.branch2.leaf1.another_subleaf1', 'data':[]},
            ...     {'name':'root.branch2.leaf1.another_subleaf2', 'data':[]}
            ... ])
            >>> print(str(tobj))
            root
            ├branch1 (*)
            │├leaf1
            ││├subleaf1 (*)
            ││└subleaf2
            │└leaf2 (*)
            │ └subleaf2
            └branch2
             └leaf1 (*)
              ├another_subleaf1
              └another_subleaf2
            >>> tobj.flatten_subtree('root.branch1.leaf1')
            >>> print(str(tobj))
            root
            ├branch1 (*)
            │├leaf1.subleaf1 (*)
            │├leaf1.subleaf2
            │└leaf2 (*)
            │ └subleaf2
            └branch2
             └leaf1 (*)
              ├another_subleaf1
              └another_subleaf2
            >>> tobj.flatten_subtree('root.branch2.leaf1')
            >>> print(str(tobj))
            root
            ├branch1 (*)
            │├leaf1.subleaf1 (*)
            │├leaf1.subleaf2
            │└leaf2 (*)
            │ └subleaf2
            └branch2
             └leaf1 (*)
              ├another_subleaf1
              └another_subleaf2
        """
        if self._validate_node_name(name):
            raise RuntimeError("Argument `name` is not valid")
        self._node_in_tree(name)
        parent = self._db[name]["parent"]
        if (parent) and (not self._db[name]["data"]):
            children = self._db[name]["children"]
            for child in children:
                self._db[child]["parent"] = parent
            self._db[parent]["children"].remove(name)
            self._db[parent]["children"] = sorted(
                self._db[parent]["children"] + children
            )
            del self._db[name]

    def get_children(self, name):
        r"""
        Get the children node names of a node.

        :param name: Parent node name
        :type  name: :ref:`NodeName`

        :rtype: list of :ref:`NodeName`

        :raises:
         * RuntimeError (Argument \`name\` is not valid)

         * RuntimeError (Node *[name]* not in tree)
        """
        if self._validate_node_name(name):
            raise RuntimeError("Argument `name` is not valid")
        self._node_in_tree(name)
        return sorted(self._db[name]["children"])

    def get_data(self, name):
        r"""
        Get the data associated with a node.

        :param name: Node name
        :type  name: :ref:`NodeName`

        :rtype: any type or list of objects of any type

        :raises:
         * RuntimeError (Argument \`name\` is not valid)

         * RuntimeError (Node *[name]* not in tree)
        """
        if self._validate_node_name(name):
            raise RuntimeError("Argument `name` is not valid")
        self._node_in_tree(name)
        return self._db[name]["data"]

    def get_leafs(self, name):
        r"""
        Get the sub-tree leaf node(s).

        :param name: Sub-tree root node name
        :type  name: :ref:`NodeName`

        :rtype: list of :ref:`NodeName`

        :raises:
         * RuntimeError (Argument \`name\` is not valid)

         * RuntimeError (Node *[name]* not in tree)
        """
        if self._validate_node_name(name):
            raise RuntimeError("Argument `name` is not valid")
        self._node_in_tree(name)
        return [node for node in self._get_subtree(name) if self.is_leaf(node)]

    def get_node(self, name):
        r"""
        Get a tree node structure.

        The structure is a dictionary with the following keys:

         * **parent** (*NodeName*) Parent node name, :code:`''` if the
           node is the root node

         * **children** (*list of NodeName*) Children node names, an
           empty list if node is a leaf

         * **data** (*list*) Node data, an empty list if node contains no data

        :param name: Node name
        :type  name: string

        :rtype: dictionary

        :raises:
         * RuntimeError (Argument \`name\` is not valid)

         * RuntimeError (Node *[name]* not in tree)
        """
        if self._validate_node_name(name):
            raise RuntimeError("Argument `name` is not valid")
        self._node_in_tree(name)
        return self._db[name]

    def get_node_children(self, name):
        r"""
        Get the list of children structures of a node.

        See :py:meth:`ptrie.Trie.get_node` for details about the structure

        :param name: Parent node name
        :type  name: :ref:`NodeName`

        :rtype: list

        :raises:
         * RuntimeError (Argument \`name\` is not valid)

         * RuntimeError (Node *[name]* not in tree)
        """
        if self._validate_node_name(name):
            raise RuntimeError("Argument `name` is not valid")
        self._node_in_tree(name)
        return [self._db[child] for child in self._db[name]["children"]]

    def get_node_parent(self, name):
        r"""
        Get the parent structure of a node.

        See :py:meth:`ptrie.Trie.get_node` for details about the structure

        :param name: Child node name
        :type  name: :ref:`NodeName`

        :rtype: dictionary

        :raises:
         * RuntimeError (Argument \`name\` is not valid)

         * RuntimeError (Node *[name]* not in tree)
        """
        if self._validate_node_name(name):
            raise RuntimeError("Argument `name` is not valid")
        self._node_in_tree(name)
        return self._db[self._db[name]["parent"]] if not self.is_root(name) else {}

    def get_subtree(self, name):  # noqa: D302
        r"""
        Get all node names in a sub-tree.

        :param name: Sub-tree root node name
        :type  name: :ref:`NodeName`

        :rtype: list of :ref:`NodeName`

        :raises:
         * RuntimeError (Argument \`name\` is not valid)

         * RuntimeError (Node *[name]* not in tree)

        Using the same example tree created in
        :py:meth:`ptrie.Trie.add_nodes`::

            >>> from __future__ import print_function
            >>> import docs.support.ptrie_example, pprint
            >>> tobj = docs.support.ptrie_example.create_tree()
            >>> print(tobj)
            root
            ├branch1 (*)
            │├leaf1
            ││└subleaf1 (*)
            │└leaf2 (*)
            │ └subleaf2
            └branch2
            >>> pprint.pprint(tobj.get_subtree('root.branch1'))
            ['root.branch1',
             'root.branch1.leaf1',
             'root.branch1.leaf1.subleaf1',
             'root.branch1.leaf2',
             'root.branch1.leaf2.subleaf2']
        """
        if self._validate_node_name(name):
            raise RuntimeError("Argument `name` is not valid")
        self._node_in_tree(name)
        return self._get_subtree(name)

    def is_root(self, name):
        r"""
        Test if a node is the root node (node with no ancestors).

        :param name: Node name
        :type  name: :ref:`NodeName`

        :rtype: boolean

        :raises:
         * RuntimeError (Argument \`name\` is not valid)

         * RuntimeError (Node *[name]* not in tree)
        """
        if self._validate_node_name(name):
            raise RuntimeError("Argument `name` is not valid")
        self._node_in_tree(name)
        return not self._db[name]["parent"]

    def in_tree(self, name):
        r"""
        Test if a node is in the tree.

        :param name: Node name to search for
        :type  name: :ref:`NodeName`

        :rtype: boolean

        :raises: RuntimeError (Argument \`name\` is not valid)
        """
        if self._validate_node_name(name):
            raise RuntimeError("Argument `name` is not valid")
        return name in self._db

    def is_leaf(self, name):
        r"""
        Test if a node is a leaf node (node with no children).

        :param name: Node name
        :type  name: :ref:`NodeName`

        :rtype: boolean

        :raises:
         * RuntimeError (Argument \`name\` is not valid)

         * RuntimeError (Node *[name]* not in tree)
        """
        if self._validate_node_name(name):
            raise RuntimeError("Argument `name` is not valid")
        self._node_in_tree(name)
        return not self._db[name]["children"]

    def make_root(self, name):  # noqa: D302
        r"""
        Make a sub-node the root node of the tree.

        All nodes not belonging to the sub-tree are deleted

        :param name: New root node name
        :type  name: :ref:`NodeName`

        :raises:
         * RuntimeError (Argument \`name\` is not valid)

         * RuntimeError (Node *[name]* not in tree)

        Using the same example tree created in
        :py:meth:`ptrie.Trie.add_nodes`::

            >>> from __future__ import print_function
            >>> import docs.support.ptrie_example
            >>> tobj = docs.support.ptrie_example.create_tree()
            >>> print(tobj)
            root
            ├branch1 (*)
            │├leaf1
            ││└subleaf1 (*)
            │└leaf2 (*)
            │ └subleaf2
            └branch2
            >>> tobj.make_root('root.branch1')
            >>> print(tobj)
            root.branch1 (*)
            ├leaf1
            │└subleaf1 (*)
            └leaf2 (*)
             └subleaf2
        """
        if self._validate_node_name(name):
            raise RuntimeError("Argument `name` is not valid")
        if (name != self.root_name) and (self._node_in_tree(name)):
            for key in [node for node in self.nodes if node.find(name) != 0]:
                del self._db[key]
            self._db[name]["parent"] = ""
            self._root = name
            self._root_hierarchy_length = len(
                self.root_name.split(self._node_separator)
            )

    def print_node(self, name):  # noqa: D302
        r"""
        Print node information (parent, children and data).

        :param name: Node name
        :type  name: :ref:`NodeName`

        :raises:
         * RuntimeError (Argument \`name\` is not valid)

         * RuntimeError (Node *[name]* not in tree)

        Using the same example tree created in
        :py:meth:`ptrie.Trie.add_nodes`::

            >>> from __future__ import print_function
            >>> import docs.support.ptrie_example
            >>> tobj = docs.support.ptrie_example.create_tree()
            >>> print(tobj)
            root
            ├branch1 (*)
            │├leaf1
            ││└subleaf1 (*)
            │└leaf2 (*)
            │ └subleaf2
            └branch2
            >>> print(tobj.print_node('root.branch1'))
            Name: root.branch1
            Parent: root
            Children: leaf1, leaf2
            Data: [5, 7]
        """
        if self._validate_node_name(name):
            raise RuntimeError("Argument `name` is not valid")
        self._node_in_tree(name)
        node = self._db[name]
        children = (
            [self._split_node_name(child)[-1] for child in node["children"]]
            if node["children"]
            else node["children"]
        )
        data = (
            node["data"][0]
            if node["data"] and (len(node["data"]) == 1)
            else node["data"]
        )
        return (
            "Name: {node_name}\n"
            "Parent: {parent_name}\n"
            "Children: {children_list}\n"
            "Data: {node_data}".format(
                node_name=name,
                parent_name=node["parent"] if node["parent"] else None,
                children_list=", ".join(children) if children else None,
                node_data=data if data else None,
            )
        )

    def rename_node(self, name, new_name):  # noqa: D302
        r"""
        Rename a tree node.

        It is typical to have a root node name with more than one hierarchy
        level after using :py:meth:`ptrie.Trie.make_root`. In this instance the
        root node *can* be renamed as long as the new root name has the same or
        less hierarchy levels as the existing root name

        :param name: Node name to rename
        :type  name: :ref:`NodeName`

        :raises:
         * RuntimeError (Argument \`name\` is not valid)

         * RuntimeError (Argument \`new_name\` has an illegal root node)

         * RuntimeError (Argument \`new_name\` is an illegal root node name)

         * RuntimeError (Argument \`new_name\` is not valid)

         * RuntimeError (Node *[name]* not in tree)

         * RuntimeError (Node *[new_name]* already exists)

        Using the same example tree created in
        :py:meth:`ptrie.Trie.add_nodes`::

            >>> from __future__ import print_function
            >>> import docs.support.ptrie_example
            >>> tobj = docs.support.ptrie_example.create_tree()
            >>> print(tobj)
            root
            ├branch1 (*)
            │├leaf1
            ││└subleaf1 (*)
            │└leaf2 (*)
            │ └subleaf2
            └branch2
            >>> tobj.rename_node(
            ...     'root.branch1.leaf1',
            ...     'root.branch1.mapleleaf1'
            ... )
            >>> print(tobj)
            root
            ├branch1 (*)
            │├leaf2 (*)
            ││└subleaf2
            │└mapleleaf1
            │ └subleaf1 (*)
            └branch2
        """
        if self._validate_node_name(name):
            raise RuntimeError("Argument `name` is not valid")
        if self._validate_node_name(new_name):
            raise RuntimeError("Argument `new_name` is not valid")
        self._node_in_tree(name)
        if self.in_tree(new_name) and (name != self.root_name):
            raise RuntimeError("Node {0} already exists".format(new_name))
        sep = self._node_separator
        if (name.split(sep)[:-1] != new_name.split(sep)[:-1]) and (
            name != self.root_name
        ):
            raise RuntimeError("Argument `new_name` has an illegal root node")
        old_hierarchy_length = len(name.split(self._node_separator))
        new_hierarchy_length = len(new_name.split(self._node_separator))
        if (name == self.root_name) and (old_hierarchy_length < new_hierarchy_length):
            raise RuntimeError("Argument `new_name` is an illegal root node name")
        self._rename_node(name, new_name)

    def search_tree(self, name):  # noqa: D302
        r"""
        Search tree for all nodes with a specific name.

        :param name: Node name to search for
        :type  name: :ref:`NodeName`

        :raises: RuntimeError (Argument \`name\` is not valid)

        For example:

            >>> from __future__ import print_function
            >>> import pprint, ptrie
            >>> tobj = ptrie.Trie('/')
            >>> tobj.add_nodes([
            ...     {'name':'root', 'data':[]},
            ...     {'name':'root/anode', 'data':7},
            ...     {'name':'root/bnode', 'data':[]},
            ...     {'name':'root/cnode', 'data':[]},
            ...     {'name':'root/bnode/anode', 'data':['a', 'b', 'c']},
            ...     {'name':'root/cnode/anode/leaf', 'data':True}
            ... ])
            >>> print(tobj)
            root
            ├anode (*)
            ├bnode
            │└anode (*)
            └cnode
             └anode
              └leaf (*)
            >>> pprint.pprint(tobj.search_tree('anode'), width=40)
            ['root/anode',
             'root/bnode/anode',
             'root/cnode/anode',
             'root/cnode/anode/leaf']
        """
        if self._validate_node_name(name):
            raise RuntimeError("Argument `name` is not valid")
        return self._search_tree(name)

    # Managed attributes
    nodes = property(_get_nodes, doc="Trie nodes")
    """
    Gets the name of all tree nodes, :code:`None` if the tree is empty

    :rtype: list of :ref:`NodeName` or None
    """

    node_separator = property(_get_node_separator, doc="Node separator")
    """
    Gets the node separator character

    :rtype: string
    """

    root_name = property(_get_root_name, doc="Trie root node name")
    """
    Gets the tree root node name, :code:`None` if the
    :py:class:`ptrie.Trie` object has no nodes

    :rtype: :ref:`NodeName` or None
    """

    root_node = property(_get_root_node, doc="Trie root node")
    """
    Gets the tree root node structure or :code:`None`
    if :py:class:`ptrie.Trie` object has no nodes. See
    :py:meth:`ptrie.Trie.get_node` for details about returned dictionary

    :rtype: dictionary or None
    """
