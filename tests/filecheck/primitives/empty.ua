# RUN: xuiua parse %s | filecheck %s --check-prefix=AST

# AST:       [
# AST-NEXT:    Words(
# AST-NEXT:      [
# AST-NEXT:      ]
# AST-NEXT:    ),
# AST-NEXT:  ]
