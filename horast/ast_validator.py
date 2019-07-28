"""Extended AST validator."""

# pylint: disable=invalid-name

# import logging

from static_typing.ast_manipulation import AstValidator as AstValidatorBase
import typed_ast.ast3

from .nodes import Comment, Directive

TypedAstValidatorBase = AstValidatorBase[typed_ast.ast3]

# _LOG = logging.getLogger(__name__)


class AstValidator(TypedAstValidatorBase):

    statement_types = (*TypedAstValidatorBase.statement_types, Comment, Directive)

    def validate_Comment(self, comment):
        assert hasattr(comment, 'comment')
        assert isinstance(comment.comment, str), type(comment.comment)

    def validate_Directive(self, directive):
        assert hasattr(directive, 'expr')
        assert isinstance(directive.expr, str), type(directive.expr)
