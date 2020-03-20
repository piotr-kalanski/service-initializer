import unittest
from tasks.aws.cloudformation import AWS_CloudFormation_CreateStack_Task
from service_metadata.model import ServiceMetadata


class Test_CloudFormation_CreateStack_Task(unittest.TestCase):

    def test_get_stack_name(self):
        task = AWS_CloudFormation_CreateStack_Task(
            template_body='body',
            stack_parameters={},
            service_metadata_parameter_with_stack_name='cf_stack_name',
            service_metadata_parameter_with_stack_parameters='',
        )

        sm = ServiceMetadata(
            name="name",
            description="description",
            parameters={
                "cf_stack_name": "stack_name"
            }
        )

        self.assertEqual("stack_name", task._get_stack_name(sm))

    def test_get_parameters_only_basic_parameters(self):
        task = AWS_CloudFormation_CreateStack_Task(
            template_body='body',
            service_metadata_parameter_with_stack_name='cf_stack_name',
            stack_parameters={
                'p1': 'v1',
                'p2': 'v2',
            }
        )

        sm = ServiceMetadata(
            name="name",
            description="description",
            parameters={}
        )

        expected_parameters = [
            {
                'ParameterKey': 'p1',
                'ParameterValue': 'v1',
            },
            {
                'ParameterKey': 'p2',
                'ParameterValue': 'v2',
            }
        ]

        self.assertEqual(expected_parameters, task._get_stack_parameters(sm))

    def test_get_parameters_only_from_service_metadata(self):
        task = AWS_CloudFormation_CreateStack_Task(
            template_body='body',
            service_metadata_parameter_with_stack_name='cf_stack_name',
            service_metadata_parameter_with_stack_parameters='cf_stack_parameters',
        )

        sm = ServiceMetadata(
            name="name",
            description="description",
            parameters={
                'cf_stack_parameters': {
                    'p1': 'v11',
                    'p2': 'v22',
                }
            }
        )

        expected_parameters = [
            {
                'ParameterKey': 'p1',
                'ParameterValue': 'v11',
            },
            {
                'ParameterKey': 'p2',
                'ParameterValue': 'v22',
            }
        ]

        self.assertEqual(expected_parameters, task._get_stack_parameters(sm))

    def test_get_parameters_complex(self):
        task = AWS_CloudFormation_CreateStack_Task(
            template_body='body',
            service_metadata_parameter_with_stack_name='cf_stack_name',
            service_metadata_parameter_with_stack_parameters='cf_stack_parameters',
            stack_parameters={
                'p1': 'v1',
                'p2': 'v2',
            }
        )

        sm = ServiceMetadata(
            name="name",
            description="description",
            parameters={
                'cf_stack_parameters': {
                    'p2': 'v22',
                    'p3': 'v33',
                }
            }
        )

        expected_parameters = [
            {
                'ParameterKey': 'p1',
                'ParameterValue': 'v1',
            },
            {
                'ParameterKey': 'p2',
                'ParameterValue': 'v22',
            },
            {
                'ParameterKey': 'p3',
                'ParameterValue': 'v33',
            }
        ]

        self.assertEqual(expected_parameters, task._get_stack_parameters(sm))        
