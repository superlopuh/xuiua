# RUN: xuiua parse %s | filecheck %s --check-prefix=AST
# RUN: xuiua lower %s | filecheck %s --check-prefix=IR-GEN

Hello ←

# AST:       [
# AST-NEXT:    Binding(
# AST-NEXT:      name: Hello,
# AST-NEXT:      public: True,
# AST-NEXT:      array_macro: False,
# AST-NEXT:      signature: None
# AST-NEXT:      words: [
# AST-NEXT:      ],
# AST-NEXT:    )
# AST-NEXT:  ]

# IR-GEN:       builtin.module {
# IR-GEN-NEXT:    func.func @Hello() {
# IR-GEN-NEXT:      func.return
# IR-GEN-NEXT:    }
# IR-GEN-NEXT:  }
