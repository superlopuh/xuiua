# RUN: xuiua parse %s | filecheck %s --check-prefix=AST

1 2
1 [2 3 4]
[1 2 3] [4 5 6]

# AST:       [
# AST-NEXT:    Words(
# AST-NEXT:      [
# AST-NEXT:        [
# AST-NEXT:          57-58: "1",
# AST-NEXT:          58-59: <spaces>,
# AST-NEXT:          59-60: "2",
# AST-NEXT:        ],
# AST-NEXT:        [
# AST-NEXT:          61-62: "1",
# AST-NEXT:          62-63: <spaces>,
# AST-NEXT:          63-70: arr(
# AST-NEXT:            "2",
# AST-NEXT:            <spaces>,
# AST-NEXT:            "3",
# AST-NEXT:            <spaces>,
# AST-NEXT:            "4",
# AST-NEXT:          ),
# AST-NEXT:        ],
# AST-NEXT:        [
# AST-NEXT:          71-78: arr(
# AST-NEXT:            "1",
# AST-NEXT:            <spaces>,
# AST-NEXT:            "2",
# AST-NEXT:            <spaces>,
# AST-NEXT:            "3",
# AST-NEXT:          ),
# AST-NEXT:          78-79: <spaces>,
# AST-NEXT:          79-86: arr(
# AST-NEXT:            "4",
# AST-NEXT:            <spaces>,
# AST-NEXT:            "5",
# AST-NEXT:            <spaces>,
# AST-NEXT:            "6",
# AST-NEXT:          ),
# AST-NEXT:        ],
# AST-NEXT:      ]
# AST-NEXT:    ),
# AST-NEXT:  ]
