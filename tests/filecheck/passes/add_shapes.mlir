// RUN: xuiua lower %s 'add-shapes{shapes="Add=2x3_2x3;Id=4x5"}' | filecheck %s

// CHECK: @Add(%0 : tensor<2x3xf64>, %1 : tensor<2x3xf64>) -> tensor<*xf64>
func.func @Add(%0 : tensor<*xf64>, %1 : tensor<*xf64>) -> tensor<*xf64> {
    // CHECK-NEXT: %2 = "uiua.add"(%0, %1) : (tensor<2x3xf64>, tensor<2x3xf64>) -> tensor<*xf64>
    %2 = "uiua.add"(%0, %1) : (tensor<*xf64>, tensor<*xf64>) -> tensor<*xf64>
    // CHECK-NEXT: %3 = "uiua.cast"(%2) : (tensor<*xf64>) -> tensor<*xf64>
    // CHECK-NEXT: func.return %3 : tensor<*xf64>
    func.return %2 : tensor<*xf64>
}


// CHECK:      @Id(%0 : tensor<4x5xf64>) -> tensor<*xf64>
func.func @Id(%0 : tensor<*xf64>) -> tensor<*xf64> {
    // CHECK-NEXT: %1 = "uiua.cast"(%0) : (tensor<4x5xf64>) -> tensor<*xf64>
    // CHECK-NEXT: func.return %1 : tensor<*xf64>
    func.return %0 : tensor<*xf64>
}
