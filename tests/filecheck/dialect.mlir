// RUN: xuiua lower %s | filecheck %s

// CHECK:  %t = "test.op"() : () -> tensor<*xf64>
%t = "test.op"() : () -> tensor<*xf64>

// CHECK-NEXT:  %add = "uiua.add"(%t, %t) : (tensor<*xf64>, tensor<*xf64>) -> tensor<*xf64>
%add = "uiua.add"(%t, %t) : (tensor<*xf64>, tensor<*xf64>) -> tensor<*xf64>

// CHECK-NEXT:  %cast = "uiua.cast"(%t) : (tensor<*xf64>) -> tensor<*xf64>
%cast = "uiua.cast"(%t) : (tensor<*xf64>) -> tensor<*xf64>

// CHECK-NEXT:  %multiply = "uiua.multiply"(%t, %t) : (tensor<*xf64>, tensor<*xf64>) -> tensor<*xf64>
%multiply = "uiua.multiply"(%t, %t) : (tensor<*xf64>, tensor<*xf64>) -> tensor<*xf64>

// CHECK-NEXT:  %arg_reduce = "test.op"() : () -> tensor<2x3x4xf64>
%arg_reduce = "test.op"() : () -> tensor<2x3x4xf64>

// CHECK-NEXT:  %reduce = "uiua.reduce"(%arg_reduce) ({
// CHECK-NEXT:  ^0(%acc_reduce : tensor<5x6xf64>, %val_reduce : tensor<3x4xf64>):
%reduce = "uiua.reduce"(%arg_reduce) ({
^0(%acc_reduce : tensor<5x6xf64>, %val_reduce : tensor<3x4xf64>):
    // CHECK-NEXT:  %next_reduce = "test.op"(%acc_reduce, %val_reduce) : (tensor<5x6xf64>, tensor<3x4xf64>) -> tensor<5x6xf64>
    %next_reduce = "test.op"(%acc_reduce, %val_reduce) : (tensor<5x6xf64>, tensor<3x4xf64>) -> tensor<5x6xf64>
    // CHECK-NEXT:  "uiua.yield"(%next_reduce) : (tensor<5x6xf64>) -> ()
    "uiua.yield"(%next_reduce) : (tensor<5x6xf64>) -> ()
// CHECK-NEXT:  }) : (tensor<2x3x4xf64>) -> tensor<5x6xf64>
}) : (tensor<2x3x4xf64>) -> tensor<5x6xf64>
