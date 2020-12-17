resource "aws_iot_thing_type" "thermostat" {
  name = "thermostat"
}

resource "aws_iot_thing" "bedroom_thermostat" {
  name            = "bedroom_thermostat"
  thing_type_name = aws_iot_thing_type.thermostat.name
}

data "aws_region" "current" {}

data "aws_caller_identity" "current" {}

data "aws_iot_endpoint" "endpoint" {}

data "aws_iam_policy_document" "publishTemp" {
  statement {
    actions = [
      "iot:Publish",
      "iot:Receive"
    ]
    resources = [
      "arn:aws:iot:${data.aws_region.current.name}:${data.aws_caller_identity.current.id}:topic/tempReading/*"
    ]
    effect = "Allow"
  }

  statement {
    actions = [
      "iot:Subscribe"
    ]
    resources = [
      "arn:aws:iot:${data.aws_region.current.name}:${data.aws_caller_identity.current.id}:topicfilter/tempReading/*"
    ]
    effect = "Allow"
  }

  statement {
    actions = [
      "iot:Connect"
    ]
    resources = [
      "arn:aws:iot:${data.aws_region.current.name}:${data.aws_caller_identity.current.id}:client/esp8266*"
    ]
    effect = "Allow"
  }
}

resource "aws_iot_certificate" "cert" {
  active = true
}

resource "aws_iot_policy" "publishTemp" {
  name = "publishTemp"
  policy = data.aws_iam_policy_document.publishTemp.json
}

resource "aws_iot_policy_attachment" "att" {
  policy = aws_iot_policy.publishTemp.name
  target = aws_iot_certificate.cert.arn
}

resource "aws_iot_thing_principal_attachment" "att" {
  principal = aws_iot_certificate.cert.arn
  thing     = aws_iot_thing.bedroom_thermostat.name
}

output "private_key" {
  value = aws_iot_certificate.cert.private_key
}

output "cert_pem" {
  value = aws_iot_certificate.cert.certificate_pem
}

output "iot_endpoint" {
  value = data.aws_iot_endpoint.endpoint.endpoint_address
}