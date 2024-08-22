# RUN: xuiua parse %s | filecheck %s --check-prefix=AST
# RUN: xuiua lower %s | filecheck %s --check-prefix=IR-GEN

Add ← +

# AST:       [
# AST-NEXT:    Binding(
# AST-NEXT:      name: Add,
# AST-NEXT:      public: True,
# AST-NEXT:      array_macro: False,
# AST-NEXT:      signature: None
# AST-NEXT:      words: [
# AST-NEXT:        121-122: <spaces>,
# AST-NEXT:        122-123: ADD,
# AST-NEXT:      ],
# AST-NEXT:    ),
# AST-NEXT:  ]

# IR-GEN:       builtin.module {
# IR-GEN-NEXT:    func.func @Add(%0 : tensor<*xf64>, %1 : tensor<*xf64>) -> tensor<*xf64> {
# IR-GEN-NEXT:      %2 = "uiua.add"(%0, %1) : (tensor<*xf64>, tensor<*xf64>) -> tensor<*xf64>
# IR-GEN-NEXT:      func.return %2 : tensor<*xf64>
# IR-GEN-NEXT:    }
# IR-GEN-NEXT:  }
