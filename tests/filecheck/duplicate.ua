# RUN: xuiua parse %s | filecheck %s --check-prefix=AST
[. 1 2 3 4]

# AST:       [
# AST-NEXT:    Words(
# AST-NEXT:      [
# AST-NEXT:        [
# AST-NEXT:          56-67: arr(
# AST-NEXT:            DUPLICATE,
# AST-NEXT:            <spaces>,
# AST-NEXT:            "1",
# AST-NEXT:            <spaces>,
# AST-NEXT:            "2",
# AST-NEXT:            <spaces>,
# AST-NEXT:            "3",
# AST-NEXT:            <spaces>,
# AST-NEXT:            "4",
# AST-NEXT:          ),
# AST-NEXT:        ],
# AST-NEXT:      ]
# AST-NEXT:    ),
# AST-NEXT:  ]
