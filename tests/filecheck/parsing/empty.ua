# RUN: xuiua parse %s | filecheck %s --check-prefix=AST
# RUN: xuiua lower %s uiua | filecheck %s --check-prefix=IR-GEN

# AST:       [
# AST-NEXT:  ]

# IR-GEN:       builtin.module {
# IR-GEN-NEXT:  }
