"""Definitions of AST nodes used to store missing syntax information."""

# pylint: disable=too-few-public-methods

import tokenize
import typing as t

import typed_ast.ast3


class Comment(typed_ast.ast3.AST):

    """Store code comment in AST.

    Examples:

    # full line comment

    expr # end-of-line comment

    (value1,
     # full line comment inside an expression
     value2,
     value3)

    (value1,
     value2,  # end-of line comment inside an expression
     value3)
    """

    _fields = typed_ast.ast3.AST._fields + ('comment', 'eol')

    @staticmethod
    def is_eol(token: tokenize.TokenInfo, path_to_anchor, before_anchor) -> bool:
        if before_anchor:
            return False
        assert path_to_anchor
        anchor = path_to_anchor[-1]
        assert isinstance(anchor.field, str), type(anchor.field)
        node = getattr(anchor.node, anchor.field)
        if anchor.index is not None:
            node = node[anchor.index]
        if not hasattr(node, 'lineno'):
            raise ValueError('anchor node {} must have "lineno" attribute'
                             .format(typed_ast.ast3.dump(node, include_attributes=True)))
        return node.lineno == token.start[0] and node.lineno == token.end[0]

    @classmethod
    def from_token(cls, token: tokenize.TokenInfo, path_to_anchor, before_anchor):
        eol = cls.is_eol(token, path_to_anchor, before_anchor)
        return cls(
            comment=token.string[1:], eol=eol,
            lineno=token.start[0], col_offset=token.start[1])


class BlockComment(typed_ast.ast3.AST):

    """Store sequence of code comments as a single node in AST.

    Example:

    # 1st line of a comment
    # 2nd line of a comment
    # 3rd line of a comment
    """

    _fields = typed_ast.ast3.AST._fields + ('comments',)

    @classmethod
    def from_token(cls, token: tokenize.TokenInfo, *extra_tokens: t.List[tokenize.TokenInfo]):
        raise NotImplementedError()


class Directive(typed_ast.ast3.AST):

    """Store directive in AST.

    In Python, directives would be expressed as comments, but may have special additional meaning.

    Examples:

    #if
    #endif
    #def
    #undef
    #ifdef
    """

    _fields = typed_ast.ast3.AST._fields + ('expr',)


class Pragma(Directive):

    """Store a pragma in AST.

    Examples:

    #pragma once
    #pragma ...
    # pragma: ...
    """

    pass


class OpenMpPragma(Pragma):

    """A special node for storing OpenMP pragmas in AST.

    Examples:

    #pragma omp parallel loop
    """

    pass


class OpenAccPragma(Pragma):

    """A special node for storing OpenACC pragmas in AST.

    Examples:

    #pragma acc
    """

    pass


class Include(Directive):

    """Store an include directive in AST.

    #include<cstdio>
    # include: my_header.h
    """

    pass

# class Docstring(ast.Expr):
#
#     """Store docstring as a special node in AST."""
#
#     @classmethod
#     def from_str_expr(cls, str_expr: typed_ast.ast3.Expr):
#         raise NotImplementedError()
