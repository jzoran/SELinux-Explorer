from analyzer.FileAnalyzer import *
from drawer.RelationDrawer import *
from drawer.DrawerHelper import *
from AppSetting import *
from model.PolicyEntities import *
from logic.FilterResult import *


class AnalyzerLogic:
    def __init__(self):
        super().__init__()
        self._init_variables()
        self.init_analyzer()

    def _init_variables(self):
        self.keep_result = False
        self.list_of_diagrams = []
        self.ref_policy_file = PolicyFile()
        self.drawer = RelationDrawer()

    def init_analyzer(self):
        self.analyzer = FileAnalyzer()

    def analyze_all(self, included_paths, excluded_paths):
        if self.keep_result:
            policy_files.extend(self.analyzer.analyze(included_paths, excluded_paths))
        else:
            policy_files = self.analyzer.analyze(included_paths, excluded_paths)
        self.update_statusbar("Analyze finished")
        self.ref_policy_file = self.make_ref_policy_file(policy_files)
        self.on_analyze_finished(None)
        self.update_analyzer_output_data(self.ref_policy_file)

    def make_ref_policy_file(self, policy_files):
        self.update_statusbar("Make reference policy file finished")
        if policy_files is None or len(policy_files) == 0:
            return None

        ref_policy_file = PolicyFile()
        for policy_file in policy_files:
            ref_policy_file.type_def.extend(policy_file.type_def)
            ref_policy_file.attribute.extend(policy_file.attribute)
            ref_policy_file.contexts.extend(policy_file.contexts)
            ref_policy_file.se_apps.extend(policy_file.se_apps)
            ref_policy_file.rules.extend(policy_file.rules)
            ref_policy_file.macros.extend(policy_file.macros)
            ref_policy_file.macro_calls.extend(policy_file.macro_calls)

        ref_policy_file.rules.extend(
            self.convert_macrocall_to_rule(
                ref_policy_file.macro_calls, ref_policy_file.macros
            )
        )

        return ref_policy_file

    def convert_macrocall_to_rule(self, macro_calls, macros):
        lst_rules = []

        for macro_call in macro_calls:
            # print("macroCall.name: ", macro_call.name)
            for macro in macros:
                # print("macro.name: ", macro.name)
                if macro.name == macro_call.name:
                    # print("macro.name: ", macro.name)
                    rules = macro.rules
                    for rule in rules:
                        """Need to replace $number in source, target or
                        class_type with parameter from macro call with
                         the same number"""
                        new_rule = Rule(
                            rule=rule.rule,
                            source=rule.source,
                            target=rule.target,
                            class_type=rule.class_type,
                            permissions=rule.permissions,
                        )
                        for i in range(0, len(macro_call.parameters)):
                            new_rule.source = new_rule.source.replace(
                                "$" + str(i + 1), macro_call.parameters[i]
                            )
                            new_rule.target = new_rule.target.replace(
                                "$" + str(i + 1), macro_call.parameters[i]
                            )
                            new_rule.class_type = new_rule.class_type.replace(
                                "$" + str(i), macro_call.parameters[i]
                            )
                        # print("macro_call.parameters: ", macro_call.parameters)
                        # print("rule: ", new_rule)
                        lst_rules.append(new_rule)
                    break

        return lst_rules

    def clear_output(self):
        files = SystemUtility().get_list_of_files(os.getcwd() + "/" + OUT_DIR, "*")
        for file in files:
            if os.path.isfile(file):
                SystemUtility().delete_files(file)
        self.on_analyze_finished(None)

    def clear_file_from_analyzer(self, file_path):
        self.analyzer.clear()
        SystemUtility().delete_files(generate_diagram_file_name(file_path))
        SystemUtility().delete_files(generate_puml_file_name(file_path))
        self.on_analyze_finished(None)

    def remove_file(self, file_path):
        SystemUtility().delete_files(
            os.path.splitext(file_path)[0] + DIAGRAM_FILE_EXTENSION
        )
        SystemUtility().delete_files(os.path.splitext(file_path)[0] + ".puml")

    def clear(self):
        self.ref_policy_file = PolicyFile()
        self.update_analyzer_output_data(None)

    def get_image_path(self, file_path):
        return generate_diagram_file_name(file_path)

    def set_keep_result(self, state):
        self.keep_result = state
        # print("self.keep_result:", self.keep_result)

    def set_ui_update_generated_diagrams_signal(self, _update_generated_diagram_list):
        self.update_generated_diagram_list = _update_generated_diagram_list

    def set_ui_update_analyzer_data_signal(self, _update_analyzer_output_data):
        self.update_analyzer_output_data = _update_analyzer_output_data

    def on_analyze_finished(self, filtered_policy_file):
        self.list_of_diagrams = SystemUtility().get_list_of_files(
            os.getcwd() + "/" + OUT_DIR, "*" + DIAGRAM_FILE_EXTENSION
        )
        self.update_generated_diagram_list(self.list_of_diagrams)

    def set_statusbar_update_signal(self, _update_statusbar):
        self.update_statusbar = _update_statusbar

    """This function collects all the information of a filter rule and returns it as a list of string"""

    def get_info_of_item(self, filter_rule):
        if self.ref_policy_file is None:
            return None

        lst_info = []
        filter_result = FilterResult()
        # print("filter_rule: ", filter_rule)
        if filter_rule.filter_type == FilterType.DOMAIN:
            lst_info.extend(
                filter_result.filter_se_app(filter_rule, self.ref_policy_file)
            )
            lst_info.extend(
                filter_result.filter_context(filter_rule, self.ref_policy_file)
            )
            lst_info.extend(
                filter_result.filter_context(
                    FilterRule(
                        filter_rule.filter_type,
                        filter_rule.keyword + DOMAIN_EXECUTABLE,
                        filter_rule.exact_word,
                    ),
                    self.ref_policy_file,
                )
            )
            return lst_info
        elif filter_rule.filter_type == FilterType.CLASS_TYPE:
            lst_info.extend(
                filter_result.filter_context(filter_rule, self.ref_policy_file)
            )
            lst_info.extend(
                filter_result.filter_se_app(filter_rule, self.ref_policy_file)
            )
            return lst_info
        elif filter_rule.filter_type == FilterType.FILE_PATH:
            lst_info.extend(
                filter_result.filter_context_by_pathname(
                    filter_rule, self.ref_policy_file
                )
            )
            lst_info.extend(
                filter_result.filter_se_app_by_name(filter_rule, self.ref_policy_file)
            )
            return lst_info
        else:
            return None
