// RUN: xuiua lower %s 'add-shapes{shapes="Add=2x3_2x3;Id=4x5"}' | filecheck %s

// CHECK: @Add(%0 : tensor<2x3xf64>, %1 : tensor<2x3xf64>) -> tensor<*xf64>
func.func @Add(%0 : tensor<*xf64>, %1 : tensor<*xf64>) -> tensor<*xf64> {
    %2 = "uiua.add"(%0, %1) : (tensor<*xf64>, tensor<*xf64>) -> tensor<*xf64>
    func.return %2 : tensor<*xf64>
}


// CHECK:      @Id(%0 : tensor<4x5xf64>)
// CHECK-SAME: -> tensor<4x5xf64>
func.func @Id(%0 : tensor<*xf64>) -> tensor<*xf64> {
    func.return %0 : tensor<*xf64>
}
