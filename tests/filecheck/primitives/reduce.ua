# RUN: xuiua parse %s | filecheck %s --check-prefix=AST

/+ [1 2 3 4 5]

# AST:       [
# AST-NEXT:    Words(
# AST-NEXT:      [
# AST-NEXT:        [
# AST-NEXT:          {{\d+}}-{{\d+}}: REDUCE(
# AST-NEXT:            ADD,
# AST-NEXT:          ),
# AST-NEXT:          {{\d+}}-{{\d+}}: <spaces>,
# AST-NEXT:          {{\d+}}-{{\d+}}: arr(
# AST-NEXT:            "1",
# AST-NEXT:            <spaces>,
# AST-NEXT:            "2",
# AST-NEXT:            <spaces>,
# AST-NEXT:            "3",
# AST-NEXT:            <spaces>,
# AST-NEXT:            "4",
# AST-NEXT:            <spaces>,
# AST-NEXT:            "5",
# AST-NEXT:          ),
# AST-NEXT:        ],
# AST-NEXT:      ]
# AST-NEXT:    ),
# AST-NEXT:  ]
