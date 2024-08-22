# RUN: xuiua parse %s | filecheck %s --check-prefix=AST
# RUN: xuiua lower %s uiua | filecheck %s --check-prefix=IR-GEN

1
2
3 4

# AST:       [
# AST-NEXT:    Words(
# AST-NEXT:      [
# AST-NEXT:        [
# AST-NEXT:          121-122: "1",
# AST-NEXT:        ],
# AST-NEXT:        [
# AST-NEXT:          123-124: "2",
# AST-NEXT:        ],
# AST-NEXT:        [
# AST-NEXT:          125-126: "3",
# AST-NEXT:          126-127: <spaces>,
# AST-NEXT:          127-128: "4",
# AST-NEXT:        ],
# AST-NEXT:      ]
# AST-NEXT:    ),
# AST-NEXT:  ]

# IR-GEN:       builtin.module {
# IR-GEN-NEXT:    func.func @uiua_main() -> (tensor<1xf64>, tensor<1xf64>, tensor<1xf64>, tensor<1xf64>) {
# IR-GEN-NEXT:      %0 = arith.constant dense<1.000000e+00> : tensor<1xf64>
# IR-GEN-NEXT:      %1 = arith.constant dense<2.000000e+00> : tensor<1xf64>
# IR-GEN-NEXT:      %2 = arith.constant dense<4.000000e+00> : tensor<1xf64>
# IR-GEN-NEXT:      %3 = arith.constant dense<3.000000e+00> : tensor<1xf64>
# IR-GEN-NEXT:      func.return %0, %1, %2, %3 : tensor<1xf64>, tensor<1xf64>, tensor<1xf64>, tensor<1xf64>
# IR-GEN-NEXT:    }
# IR-GEN-NEXT:  }
