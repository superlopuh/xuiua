# RUN: xuiua parse %s | filecheck %s --check-prefix=AST
∘ 5

# AST:       [
# AST-NEXT:    Words(
# AST-NEXT:      [
# AST-NEXT:        [
# AST-NEXT:          56-57: IDENTITY,
# AST-NEXT:          57-58: <spaces>,
# AST-NEXT:          58-59: "5",
# AST-NEXT:        ],
# AST-NEXT:      ]
# AST-NEXT:    ),
# AST-NEXT:  ]
