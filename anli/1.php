<?php
header('Content-Type: application/json');

// 获取 POST 参数
$postData = json_decode(file_get_contents("php://input"), true);

// 检查是否接收到有效数据
if (isset($postData['encodedData'])) {
    // 获取 Base64 编码的数据
    $encodedData = $postData['encodedData'];

    // 判断是否以等号("=")结尾
     if (substr($encodedData, -1) === '=') {
            // 如果以等号结尾，解码并再次进行加密传递给客户端
            $decodedData = base64_decode($encodedData);
            $decodedData = base64_encode($decodedData);
    } else {
        // 如果不是 Base64 编码，直接对原始数据进行 Base64 编码
        $decodedData = base64_encode($encodedData);
    }

    // 返回继续加密后的数据
    $response = array('reencodedData' => $decodedData);
    echo json_encode($response);
} else {
    // 返回错误信息
    $errorResponse = array('error' => 'Invalid data received');
    echo json_encode($errorResponse);
}
?>