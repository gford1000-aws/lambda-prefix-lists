# Lambda Prefix Lists

This Cloudformation script creates a Lambda function returns the Prefix List details (used for VPC Endpoints), for a user supplied region, service and data selection.  

The Lambda expects to receive an event of the form:

```
{
	"ServiceName" : "s3" | "dynamodb",
	"RegionName" : <A valid AWS Region name>,
	"Keys" : [ "Cidrs", "PrefixListId" ]
}
```

If `RegionName` is omitted, then the region of the Lambda is used.

If `Keys` is omitted, then all details for the matched Prefix List items are returned.

The script creates the following:

![alt text](https://github.com/gford1000-aws/lambda-prefix-lists/blob/master/PrefixList.png "Script per designer")


## Arguments

| Argument                      | Description                                                                     |
| ----------------------------- |:-------------------------------------------------------------------------------:|
| DefaultRegion                 | The default region (the region in which the stack is deployed)                  |
| XRayTraceMode                 | If XRay tracing is enabled, then this parameter specifies the type of tracing   |


## Outputs

| Output               | Description                                            |
| ---------------------|:------------------------------------------------------:|
| Lambda               | The Arn of the Lambda function                         |


## Licence

This project is released under the MIT license. See [LICENSE](LICENSE) for details.
