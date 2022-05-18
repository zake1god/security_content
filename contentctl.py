import sys
import argparse
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'bin/contentctl_project')))

from bin.contentctl_project.contentctl_core.application.use_cases.content_changer import ContentChanger, ContentChangerInputDto
from bin.contentctl_project.contentctl_core.application.use_cases.generate import GenerateInputDto, Generate
from bin.contentctl_project.contentctl_core.application.use_cases.validate import ValidateInputDto, Validate
from bin.contentctl_project.contentctl_core.application.use_cases.doc_gen import DocGenInputDto, DocGen
from bin.contentctl_project.contentctl_core.application.use_cases.new_content import NewContentInputDto, NewContent
from bin.contentctl_project.contentctl_core.application.use_cases.reporting import ReportingInputDto, Reporting
from bin.contentctl_project.contentctl_core.application.use_cases.initialize import Initialize
from bin.contentctl_project.contentctl_core.application.use_cases.deploy import Deploy
from bin.contentctl_project.contentctl_core.application.use_cases.build import Build
from bin.contentctl_project.contentctl_core.application.use_cases.inspect import Inspect
from bin.contentctl_project.contentctl_core.application.factory.factory import FactoryInputDto
from bin.contentctl_project.contentctl_core.application.factory.ba_factory import BAFactoryInputDto
from bin.contentctl_project.contentctl_core.application.factory.new_content_factory import NewContentFactoryInputDto
from bin.contentctl_project.contentctl_core.application.factory.object_factory import ObjectFactoryInputDto
from bin.contentctl_project.contentctl_infrastructure.builder.security_content_object_builder import SecurityContentObjectBuilder
from bin.contentctl_project.contentctl_infrastructure.builder.security_content_director import SecurityContentDirector
from bin.contentctl_project.contentctl_infrastructure.adapter.obj_to_yml_adapter import ObjToYmlAdapter
from bin.contentctl_project.contentctl_infrastructure.adapter.obj_to_json_adapter import ObjToJsonAdapter
from bin.contentctl_project.contentctl_infrastructure.builder.security_content_story_builder import SecurityContentStoryBuilder
from bin.contentctl_project.contentctl_infrastructure.builder.security_content_detection_builder import SecurityContentDetectionBuilder
from bin.contentctl_project.contentctl_infrastructure.builder.security_content_basic_builder import SecurityContentBasicBuilder
from bin.contentctl_project.contentctl_infrastructure.builder.security_content_investigation_builder import SecurityContentInvestigationBuilder
from bin.contentctl_project.contentctl_infrastructure.builder.security_content_baseline_builder import SecurityContentBaselineBuilder
from bin.contentctl_project.contentctl_infrastructure.builder.security_content_playbook_builder import SecurityContentPlaybookBuilder
from bin.contentctl_project.contentctl_core.domain.entities.enums.enums import SecurityContentProduct
from bin.contentctl_project.contentctl_infrastructure.adapter.obj_to_conf_adapter import ObjToConfAdapter
from bin.contentctl_project.contentctl_infrastructure.adapter.obj_to_md_adapter import ObjToMdAdapter
from bin.contentctl_project.contentctl_infrastructure.adapter.obj_to_svg_adapter import ObjToSvgAdapter
from bin.contentctl_project.contentctl_infrastructure.adapter.obj_to_attack_nav_adapter import ObjToAttackNavAdapter
from bin.contentctl_project.contentctl_infrastructure.builder.attack_enrichment import AttackEnrichment
from bin.contentctl_project.contentctl_core.domain.entities.enums.enums import SecurityContentType


def init():

    print("""
Running Splunk Security Content Control Tool (contentctl) 
starting program loaded for TIE Fighter...
      _                                            _
     T T                                          T T
     | |                                          | |
     | |                                          | |
     | |                                          | |
     | |                                          | |
     | |                                          | |
     | |                                          | |
     | |                   ____                   | |
     | |            ___.r-"`--'"-r.____           | |
     | |.-._,.,---~"_/_/  .----.  \_\_"~---,.,_,-.| |
     | ]|.[_]_ T~T[_.-Y  / \  / \  Y-._]T~T _[_].|| |
    [|-+[  ___]| [__  |-=[--()--]=-|  __] |[___  ]+-|]
     | ]|"[_]  l_j[_"-l  \ /  \ /  !-"_]l_j  [_]~|| |
     | |`-' "~"---.,_\\"\  "o--o"  /"/_,.---"~" `-'| |
     | |             ~~"^-.____.-^"~~             | |
     | |                                          | |
     | |                                          | |
     | |                                          | |
     | |                                          | |
     | |                                          | |
     | |                                          | |
     | |                                          | |
     l_i                                          l_j -Row

    """)


def content_changer(args) -> None:
    factory_input_dto = ObjectFactoryInputDto(
        os.path.abspath(args.path),
        SecurityContentObjectBuilder(),
        SecurityContentDirector()
    )

    input_dto = ContentChangerInputDto(
        ObjToYmlAdapter(),
        factory_input_dto,
        args.change_function
    )

    content_changer = ContentChanger()
    content_changer.execute(input_dto)


def generate(args) -> None:
    if not args.product:
        print("ERROR: missing parameter -p/--product .")
        sys.exit(1)     

    #For now, the custom product is treated just like ESCU
    if args.product == 'CUSTOM':
        args.product = 'ESCU'
    
    if args.product not in ['ESCU', 'SSA', 'API']:
        print("ERROR: invalid product. valid products are ESCU, SSA or API.")
        sys.exit(1)

    factory_input_dto = FactoryInputDto(
        os.path.abspath(args.path),
        SecurityContentBasicBuilder(),
        SecurityContentDetectionBuilder(),
        SecurityContentStoryBuilder(),
        SecurityContentBaselineBuilder(),
        SecurityContentInvestigationBuilder(),
        SecurityContentPlaybookBuilder(),
        SecurityContentDirector(),
        AttackEnrichment.get_attack_lookup(store_csv=True)
    )

    ba_factory_input_dto = BAFactoryInputDto(
        os.path.abspath(args.path),
        SecurityContentBasicBuilder(),
        SecurityContentDetectionBuilder(),
        SecurityContentDirector()
    )

    if args.product == "ESCU":
        generate_input_dto = GenerateInputDto(
            os.path.abspath(args.output),
            factory_input_dto,
            ba_factory_input_dto,
            ObjToConfAdapter(),
            SecurityContentProduct.ESCU
        )
    elif args.product == "API":
        generate_input_dto = GenerateInputDto(
            os.path.abspath(args.output),
            factory_input_dto,
            ba_factory_input_dto,
            ObjToJsonAdapter(),
            SecurityContentProduct.API
        )
    else:
        generate_input_dto = GenerateInputDto(
            os.path.abspath(args.output),
            factory_input_dto,
            ba_factory_input_dto,
            ObjToYmlAdapter(),
            SecurityContentProduct.SSA
        ) 

    generate = Generate()
    generate.execute(generate_input_dto)


def validate(args) -> None:
    if not args.product:
        print("ERROR: missing parameter -p/--product .")
        sys.exit(1)     

    #For now, the custom product is treated just like ESCU
    if args.product == 'CUSTOM':
        args.product = 'ESCU'

    if args.product not in ['ESCU', 'SSA', 'all']:
        print("ERROR: invalid product. valid products are all, ESCU or SSA.")
        sys.exit(1)
    

    factory_input_dto = FactoryInputDto(
        os.path.abspath(args.path),
        SecurityContentBasicBuilder(),
        SecurityContentDetectionBuilder(),
        SecurityContentStoryBuilder(),
        SecurityContentBaselineBuilder(),
        SecurityContentInvestigationBuilder(),
        SecurityContentPlaybookBuilder(),
        SecurityContentDirector(),
        AttackEnrichment.get_attack_lookup()
    )

    ba_factory_input_dto = BAFactoryInputDto(
        os.path.abspath(args.path),
        SecurityContentBasicBuilder(),
        SecurityContentDetectionBuilder(),
        SecurityContentDirector()
    )

    if args.product == "ESCU" or args.product == "all":
        validate_input_dto = ValidateInputDto(
            factory_input_dto,
            ba_factory_input_dto,
            SecurityContentProduct.ESCU
        )
        validate = Validate()
        validate.execute(validate_input_dto)

    if args.product == "SSA" or args.product == "all":
        validate_input_dto = ValidateInputDto(
            factory_input_dto,
            ba_factory_input_dto,
            SecurityContentProduct.SSA
        )
        validate = Validate()
        validate.execute(validate_input_dto)



def doc_gen(args) -> None:
    factory_input_dto = FactoryInputDto(
        os.path.abspath(args.path),
        SecurityContentBasicBuilder(),
        SecurityContentDetectionBuilder(),
        SecurityContentStoryBuilder(),
        SecurityContentBaselineBuilder(),
        SecurityContentInvestigationBuilder(),
        SecurityContentPlaybookBuilder(),
        SecurityContentDirector(),
        AttackEnrichment.get_attack_lookup()
    )

    doc_gen_input_dto = DocGenInputDto(
        os.path.abspath(args.output),
        factory_input_dto,
        ObjToMdAdapter()
    )

    doc_gen = DocGen()
    doc_gen.execute(doc_gen_input_dto)


def new_content(args) -> None:
    if args.type == 'detection':
        content_type = SecurityContentType.detections
    elif args.type == 'story':
        content_type = SecurityContentType.stories
    else:
        print("ERROR: type " + args.type + " not supported")
        sys.exit(1)

    new_content_factory_input_dto = NewContentFactoryInputDto(content_type)
    new_content_input_dto = NewContentInputDto(new_content_factory_input_dto, ObjToYmlAdapter())
    new_content = NewContent()
    new_content.execute(new_content_input_dto)


def reporting(args) -> None:
    factory_input_dto = FactoryInputDto(
        os.path.abspath(args.path),
        SecurityContentBasicBuilder(),
        SecurityContentDetectionBuilder(),
        SecurityContentStoryBuilder(),
        SecurityContentBaselineBuilder(),
        SecurityContentInvestigationBuilder(),
        SecurityContentPlaybookBuilder(),
        SecurityContentDirector(),
        AttackEnrichment.get_attack_lookup()
    )

    reporting_input_dto = ReportingInputDto(
        factory_input_dto,
        ObjToSvgAdapter(),
        ObjToAttackNavAdapter()
    )

    reporting = Reporting()
    reporting.execute(reporting_input_dto)


def initialize(args) -> None:
    Initialize(args)


def build(args) -> None:
    Build(args)

def inspect(args) -> None:
    Inspect(args)

def cloud_deploy(args) -> None:
    Deploy(args)

def main(args):

    init()

    # grab arguments
    parser = argparse.ArgumentParser(
        description="Use `contentctl.py action -h` to get help with any Splunk Security Content action")
    parser.add_argument("-p", "--path", required=True, 
                                        help="path to the Splunk Security Content folder")
    parser.set_defaults(func=lambda _: parser.print_help())

    actions_parser = parser.add_subparsers(title="Splunk Security Content actions", dest="action")
    #new_parser = actions_parser.add_parser("new", help="Create new content (detection, story, baseline)")
    validate_parser = actions_parser.add_parser("validate", help="Validates written content")
    generate_parser = actions_parser.add_parser("generate", help="Generates a deployment package for different platforms (splunk_app)")
    content_changer_parser = actions_parser.add_parser("content_changer", help="Change Security Content based on defined rules")
    docgen_parser = actions_parser.add_parser("docgen", help="Generates documentation")
    new_content_parser = actions_parser.add_parser("new_content", help="Create new security content object")
    reporting_parser = actions_parser.add_parser("reporting", help="Create security content reporting")
    init_parser = actions_parser.add_parser("init", help="Initialize a repo with scaffolding in place to build a custom app."
                                                            "This allows a user to easily add their own content and, eventually, "
                                                            "build a custom application consisting of their custom content.")

    build_parser = actions_parser.add_parser("build", help="Build an application suitable for deployment to a search head")
    inspect_parser = actions_parser.add_parser("inspect", help="Run appinspect to ensure that an app meets minimum requirements for deployment.")

    cloud_deploy_parser = actions_parser.add_parser("cloud_deploy", help="Install an application on a target Splunk Cloud Instance.")

    # # new arguments
    # new_parser.add_argument("-t", "--type", required=False, type=str, default="detection",
    #                              help="Type of new content to create, please choose between `detection`, `baseline` or `story`. Defaults to `detection`")
    # new_parser.add_argument("-x", "--example_only", required=False, action='store_true',
    #                              help="Generates an example content UPDATE on the fields that need updating. Use `git status` to see what specific files are added. Skips new content wizard prompts.")
    # new_parser.set_defaults(func=new)

    validate_parser.add_argument("-pr", "--product", required=True, type=str, default='all', 
        help="Type of package to create, choose between all, `ESCU` or `SSA`.")
    validate_parser.set_defaults(func=validate, epilog="""
                Validates security manifest for correctness, adhering to spec and other common items.""")

    generate_parser.add_argument("-o", "--output", required=True, type=str,
        help="Path where to store the deployment package")
    generate_parser.add_argument("-pr", "--product", required=True, type=str,
        help="Type of package to create, choose between `ESCU`, `SSA` or `API`.")
    generate_parser.set_defaults(func=generate)
    
    content_changer_parser.add_argument("-cf", "--change_function", required=True, type=str,
        help="Define a change funtion defined in bin/contentctl_core/contentctl/application/use_cases/content_changer.py")
    content_changer_parser.set_defaults(func=content_changer)

    docgen_parser.add_argument("-o", "--output", required=True, type=str,
        help="Path where to store the documentation")
    docgen_parser.set_defaults(func=doc_gen)

    new_content_parser.add_argument("-t", "--type", required=True, type=str,
        help="Type of security content object, choose between `detection`, `story`")
    new_content_parser.set_defaults(func=new_content)

    reporting_parser.set_defaults(func=reporting)

    init_parser.add_argument("-t", "--title", type=str, required=True, help="The title of the application to be built.")
    init_parser.add_argument("-n", "--name", type=str, required=True, help="The name of the application to be built.")
    init_parser.add_argument("-v", "--version", type=str, required=True, help="The version of the application to be built.  It should be in MAJOR.MINOR.PATCH format.")
    init_parser.add_argument("-a", "--author_name", type=str, required=True, help="The name of the application author.")
    init_parser.add_argument("-e", "--author_email", type=str, required=True, help="The email of the application author.")
    init_parser.add_argument("-c", "--author_company", type=str, required=True, help="The company of the application author.")
    init_parser.add_argument("-d", "--description", type=str, required=True, help="A brief description of the app.")
    init_parser.set_defaults(func=initialize)

    build_parser.add_argument("-o", "--output_dir", required=False, default="build", type=str, help="Directory to output the built package to.")
    build_parser.add_argument("-pr", "--product", required=True, type=str, help="Name of the product to build.")
    build_parser.set_defaults(func=build)


    inspect_parser.add_argument("-p", "--package_path", required=True, type=str, help="Path to the package to be inspected")
    inspect_parser.set_defaults(func=inspect)

    
    cloud_deploy_parser.add_argument("--app-package", required=True, type=str, help="Path to the package you wish to deploy")
    cloud_deploy_parser.add_argument("--acs-legal-ack", required=True, type=str, help="specify '--acs-legal-ack=Y' to acknowledge your acceptance of any risks (required)")
    cloud_deploy_parser.add_argument("--username", required=True, type=str, help="splunk.com username")
    cloud_deploy_parser.add_argument("--password", required=True, type=str, help="splunk.com password")
    cloud_deploy_parser.add_argument("--server", required=False, default="https://admin.splunk.com", type=str, help="Override server URL (default 'https://admin.splunk.com')")
    cloud_deploy_parser.set_defaults(func=cloud_deploy)

    # # parse them
    args = parser.parse_args()
    try:
        return args.func(args)
    except Exception as e:
        print(f"Error for function [{args.func.__name__}]: {str(e)}")

if __name__ == "__main__":
    main(sys.argv[1:])