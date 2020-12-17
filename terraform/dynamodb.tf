resource "aws_dynamodb_table" "iot-temp" {
  name         = "iot-temp"
  billing_mode = "PROVISIONED"
  hash_key     = "timestamp"
  write_capacity = 5
  read_capacity = 5

  attribute {
    name = "timestamp"
    type = "S"
  }
}
