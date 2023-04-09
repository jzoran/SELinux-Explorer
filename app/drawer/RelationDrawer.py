from model.PolicyEntities import *
from PythonUtilityClasses import FileWriter as FW
from datetime import *
from drawer.DrawerHelper import *
from AppSetting import *
from drawer.AbstractDrawer import *

class RelationDrawer(AbstractDrawer):

    def draw_uml(self, policyFile: PolicyFile):
        self.dict_of_participant = {}
        self.drawer_class = DrawerClass()

        plant_uml_list = []
        plant_uml_list.append("@startuml")

        self.dump_policy_file(policyFile)
        plant_uml_list.extend(self.drawer_class.participants)
        plant_uml_list.extend(self.drawer_class.rules)

        plant_uml_list.append("@enduml")

        # Remove redundance items
        plant_uml_list = list(dict.fromkeys(plant_uml_list))
        # print(plant_uml_list)
        file_path = OUT_DIR + "seq_" + generate_puml_file_name(policyFile.file_name)
        self.write_to_file(file_path, plant_uml_list)
        print("drawing: ", file_path)
        generate_png(file_path)

    def draw_list_of_uml(self, policy_files: List[PolicyFile]):
        self.dict_of_participant = {}
        self.drawer_class = DrawerClass()

        plant_uml_list = []
        plant_uml_list.extend(DrawingTool.generate_start_of_puml())

        for policy_file in policy_files:
            self.dump_policy_file(policy_file)

        plant_uml_list.extend(self.drawer_class.participants)
        plant_uml_list.extend(self.drawer_class.rules)

        plant_uml_list.extend(DrawingTool.generate_end_of_puml())

        # Remove redundance items
        plant_uml_list = list(dict.fromkeys(plant_uml_list))
        # print(plant_uml_list)
        file_path = OUT_DIR + "/Integrated-" + \
            datetime.today().strftime("%d-%m-%y---%H-%M-%s") + "_relation.puml"
        '''self.writeToFile(file_path, plant_uml_list)
        print("drawing: ", file_path)'''

        if not self.disable_drawing:
            self.generate_png(file_path)
        # print(policy_file)

    def draw_type_def(self, typeDefs: List[TypeDef]):
        type_def_list = []
        for type_def in typeDefs:
            # type_def.append("\"" + type_def.name + "\" -----> \"" + type_def.types + "\"" )
            type_def_list.append(
                "participant " +
                self.insert_new_participant(
                    type_def.name) +
                " [\n=" +
                type_def.name +
                "\n ----- \n\"\"" +
                ', '.join(
                    type_def.types) +
                "\"\"\n]")
        return type_def_list

    def draw_context(self, contexts: List[Context]):
        context_list = []
        for context in contexts:
            context_list.append(
                "participant " +
                self.insert_new_participant(
                    context.security_context.type) +
                " [\n=" +
                context.security_context.type +
                "\n ----- \n\"\"" +
                context.path_name +
                "\"\"\n]")
        return context_list

    def draw_se_app(self, se_app_contexts: List[SeAppContext]):
        se_app_list = []
        for se_app_context in se_app_contexts:
            se_app_list.append(
                "participant " +
                self.insert_new_participant(
                    se_app_context.domain) +
                " [\n=" +
                se_app_context.domain +
                "\n ----- \n\"\"" +
                se_app_context.user +
                "\"\"\n]")
        return se_app_list

    def draw_rule(self, rules: List[Rule]):
        rule_list = []
        for rule in rules:
            if rule.rule == RuleEnum.NEVER_ALLOW:
                rule_list.append(
                    "" +
                    self.insert_new_participant(
                        rule.source) +
                    " -----[#red]>x \"" +
                    rule.target +
                    "\" : " +
                    rule.rule.label +
                    " (" +
                    ', '.join(
                        rule.permissions) +
                    ")")
            else:
                rule_list.append(
                    "" +
                    self.insert_new_participant(
                        rule.source) +
                    " -----[#green]> \"" +
                    rule.target +
                    "\" : " +
                    rule.rule.label +
                    " (" +
                    ', '.join(
                        rule.permissions) +
                    ")")

        return rule_list

    def write_to_file(self, file_name, list_of_str):
        file_write = FW.FileWriter
        file_write.write_list_to_file(file_name, list_of_str)


