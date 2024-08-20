# RUN: xuiua parse %s | filecheck %s --check-prefix=AST

+ 1 2
+ 1 [2 3 4]
+ [1 2 3] [4 5 6]

# AST:       [
# AST-NEXT:    Words(
# AST-NEXT:      [
# AST-NEXT:        [
# AST-NEXT:          56-57: <spaces>,
# AST-NEXT:          57-58: ADD,
# AST-NEXT:          58-59: <spaces>,
# AST-NEXT:          59-60: "1",
# AST-NEXT:          60-61: <spaces>,
# AST-NEXT:          61-62: "2",
# AST-NEXT:          62-63: <spaces>,
# AST-NEXT:          63-64: ADD,
# AST-NEXT:          64-65: <spaces>,
# AST-NEXT:          65-66: "1",
# AST-NEXT:          66-67: <spaces>,
# AST-NEXT:          67-74: arr(
# AST-NEXT:            "2",
# AST-NEXT:            <spaces>,
# AST-NEXT:            "3",
# AST-NEXT:            <spaces>,
# AST-NEXT:            "4",
# AST-NEXT:          ),
# AST-NEXT:          74-75: <spaces>,
# AST-NEXT:          75-76: ADD,
# AST-NEXT:          76-77: <spaces>,
# AST-NEXT:          77-84: arr(
# AST-NEXT:            "1",
# AST-NEXT:            <spaces>,
# AST-NEXT:            "2",
# AST-NEXT:            <spaces>,
# AST-NEXT:            "3",
# AST-NEXT:          ),
# AST-NEXT:          84-85: <spaces>,
# AST-NEXT:          85-92: arr(
# AST-NEXT:            "4",
# AST-NEXT:            <spaces>,
# AST-NEXT:            "5",
# AST-NEXT:            <spaces>,
# AST-NEXT:            "6",
# AST-NEXT:          ),
# AST-NEXT:          92-93: <spaces>,
# AST-NEXT:          93-94: <spaces>,
# AST-NEXT:        ],
# AST-NEXT:      ]
# AST-NEXT:    ),
# AST-NEXT:  ]
