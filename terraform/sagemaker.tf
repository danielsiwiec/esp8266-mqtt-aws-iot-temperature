resource "aws_sagemaker_notebook_instance" "temp-vis" {
  name          = "temp-vis"
  role_arn      = aws_iam_role.sagemaker_role.arn
  instance_type = "ml.t2.medium"
}

resource "aws_iam_role" "sagemaker_role" {
  name = "sagemaker_role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "sagemaker.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "scan_temp_table_role" {
  name = "scan_temp_table_role"
  role = aws_iam_role.sagemaker_role.id

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "dynamodb:Scan"
            ],
            "Resource": "${aws_dynamodb_table.iot-temp.arn}"
        }
    ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "sagemaker-full-access" {
  role       = aws_iam_role.sagemaker_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSageMakerFullAccess"
}
