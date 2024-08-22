# RUN: xuiua parse %s | filecheck %s --check-prefix=AST
# RUN: xuiua lower %s uiua | filecheck %s --check-prefix=IR-GEN

Add ← +

# AST:       [
# AST-NEXT:    Binding(
# AST-NEXT:      name: Add,
# AST-NEXT:      public: True,
# AST-NEXT:      array_macro: False,
# AST-NEXT:      signature: None
# AST-NEXT:      words: [
# AST-NEXT:        126-127: <spaces>,
# AST-NEXT:        127-128: ADD,
# AST-NEXT:      ],
# AST-NEXT:    ),
# AST-NEXT:  ]

# IR-GEN:       builtin.module {
# IR-GEN-NEXT:    func.func @Add(%0 : tensor<*xf64>, %1 : tensor<*xf64>) {
# IR-GEN-NEXT:      %2 = "uiua.add"(%0, %1) : (tensor<*xf64>, tensor<*xf64>) -> tensor<*xf64>
# IR-GEN-NEXT:      func.return
# IR-GEN-NEXT:    }
# IR-GEN-NEXT:  }
