// RUN: xuiua lower %s 'remove-casts' | filecheck %s

func.func @Add(%0 : tensor<2x3xf64>, %1 : tensor<2x3xf64>) -> tensor<*xf64> {
    %2 = "uiua.add"(%0, %1) : (tensor<2x3xf64>, tensor<2x3xf64>) -> tensor<2x3xf64>
    %3 = "uiua.cast"(%2) : (tensor<2x3xf64>) -> tensor<*xf64>
    func.return %3 : tensor<*xf64>
}

// CHECK:       builtin.module {
// CHECK-NEXT:    func.func @Add(%0 : tensor<2x3xf64>, %1 : tensor<2x3xf64>) -> tensor<2x3xf64> {
// CHECK-NEXT:      %2 = "uiua.add"(%0, %1) : (tensor<2x3xf64>, tensor<2x3xf64>) -> tensor<2x3xf64>
// CHECK-NEXT:      func.return %2 : tensor<2x3xf64>
// CHECK-NEXT:    }
// CHECK-NEXT:  }
