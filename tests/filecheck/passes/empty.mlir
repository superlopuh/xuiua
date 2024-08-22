// RUN: xuiua lower %s | filecheck %s

module {}

// CHECK:      builtin.module {
// CHECK-NEXT: }
