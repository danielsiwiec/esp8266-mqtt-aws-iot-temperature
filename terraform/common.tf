provider "aws" {
  region = "us-west-2"
}

variable "common_tags" {
  type = map(string)
}