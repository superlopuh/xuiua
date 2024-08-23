# RUN: xuiua parse %s | filecheck %s --check-prefix=AST

(1)

# AST:       [
# AST-NEXT:    Words(
# AST-NEXT:      [
# AST-NEXT:        [
# AST-NEXT:          {{\d+}}-{{\d+}}: func(
# AST-NEXT:            "1",
# AST-NEXT:          ),
# AST-NEXT:        ],
# AST-NEXT:      ]
# AST-NEXT:    ),
# AST-NEXT:  ]
