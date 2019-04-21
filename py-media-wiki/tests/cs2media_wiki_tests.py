""" test method: tests for cs2media_wiki.py """
import unittest
# from defusedxml.ElementTree import parse
import defusedxml.ElementTree as ET
import cs2media_wiki
#
class MediawikiTests(unittest.TestCase):
    """ class: """
    #
    def setUp(self):
        self.wiki = cs2media_wiki.CS2MediaWiki()
        self.wiki.name_space = ""
        self.member01 = """<member name="M:NSG.Library.Helpers.Config.GetIntAppSettingConfigValue(System.String,System.Int32)">
            <summary>
            Get a value from the AppSetting section of the web config.
            </summary>
            <param name="configAppKey">AppSetting key value</param>
            <param name="defaultValue">if not found return this integer value</param>
            <returns>integer value in the appSetting section in the config file.</returns>
        </member>"""
        self.summary01 = """<member name="T:Library.Helpers.NamespaceDoc">
        <summary>
        The <see cref="N:Library.Helpers"/> namespace contains a
        collection of static helper methods.
        </summary></member>"""
    #
    def test_header_1(self):
        """ test method: process child assembly, making it a level 1 header. """
        label = "Hello"
        hdr = self.wiki.header(label, 1)
        print(hdr)
        self.assertEqual(hdr, "= " + label + " =")
    #
    def test_header_7(self):
        """ test method: process child assembly, making it a level 1 header. """
        label = "Hello"
        hdr = self.wiki.header(label, 7)
        print(hdr)
        self.assertEqual(hdr, "====== " + label + " ======")
    #
    def test_italic(self):
        """ test method: process child assembly, making it a level 1 header. """
        label = "Hello"
        itlc = self.wiki.italic_text(label)
        print(itlc)
        self.assertEqual(itlc, "''" + label + "''")
    #
    def test_bold(self):
        """ test method: process child assembly, making it a level 1 header. """
        label = "Hello"
        bld = self.wiki.bold_text(label)
        print(bld)
        self.assertEqual(bld, "'''" + label + "'''")
    #
    def test_text_left_trim(self):
        text = self.wiki.text_left_trim("\n   1\n   2\n   3\n   4\n")
        self.assertEqual(text, "1\n2\n3\n4")
    def test_text_left_trunc(self):
        text = self.wiki.text_left_trunc("\n   1\n   2\n   3\n   4\n", 2)
        self.assertEqual(text, "  1\n  2\n  3\n  4")
    def test_get_element_text_01(self):
        """ test method: process child assembly, making it a level 1 header. """
        member = ET.fromstring(self.summary01)
        expected = """The namespace contains a\ncollection of static helper methods."""
        txt = self.wiki.get_element_text(member.find('summary'))
        self.assertEqual(txt, expected)
    #
    def test_get_element_text_02(self):
        """ test method: process child assembly, making it a level 1 header. """
        member = ET.fromstring(self.member01)
        txt = self.wiki.get_element_text(member.find('summary'))
        print(txt)
        self.assertEqual(txt, """Get a value from the AppSetting section of the web config.""")
    #
    def test_get_element_text_03(self):
        """ test method: process child assembly, making it a level 1 header. """
        expected = """The namespace contains a\ncollection of static helper methods."""
        member = ET.fromstring(self.summary01)
        txt = self.wiki.get_element_text(member.find('summary'))
        print(txt)
        self.assertEqual(txt, expected)
    #
    def test_root_01(self):
        """ test method: highest processing loop. """
        xml_string = """<?xml version="1.0"?><doc><assembly><name>Library</name></assembly>
        <members><member name="T:Library.T"></member>
        <member name="M:Library.T.T1(System.int)"></member>
        <member name="F:Library.T.F1"></member>
        <member name="P:Library.T.Prop1"></member>
        <member name="M:Library.T.T1(System.int)"></member></members>
        </doc>"""
        doc = ET.fromstring(xml_string)
        ret = self.wiki.root(doc)
        self.assertEqual(ret, 6)
    #
    def test_assembly_name_01(self):
        """ test method: process child assembly, making it a level 1 header. """
        assm = ET.fromstring("<assembly><name>Library.Logger</name></assembly>")
        txt = self.wiki.assembly_name(assm)
        self.assertEqual(txt, "Library.Logger")
    #
    def test_get_member_attrib_name_01(self):
        """ test method: get the class/method name from the attribute. """
        xml_string = '<member name="M:Library.Helpers.GetStringApp(System.String)"></member>'
        member = ET.fromstring(xml_string)
        self.wiki.name_space = "Library.Helpers"
        txt = self.wiki.get_member_attrib_name(member)
        self.assertEqual(txt, "GetStringApp(System.String)")
    #
    def test_get_member_attrib_name_02(self):
        """ test method: get the class/method name from the attribute. """
        xml_string = '<member name="M:Library.Helpers.GetStringApp(System.String)"></member>'
        member = ET.fromstring(xml_string)
        txt = self.wiki.get_member_attrib_name(member)
        self.assertEqual(txt, "Library.Helpers.GetStringApp(System.String)")
    #
    def test_get_property_name_field_01(self):
        """ test method: get the class/method name from the attribute. """
        xml_string = '<member name="F:Library.ClassName.FieldName"></member>'
        self.wiki.full_class_name = "Library.ClassName"
        member = ET.fromstring(xml_string)
        txt = self.wiki.get_property_name(member)
        self.assertEqual(txt, "FieldName")
    #
    def test_get_property_name_prop_02(self):
        """ test method: get the class/method name from the attribute. """
        xml_string = '<member name="P:Library.ClassName.PropName"><summary>Prop Name<value>set/get string prop</value></summary></member>'
        self.wiki.full_class_name = "Library.ClassName"
        member = ET.fromstring(xml_string)
        txt = self.wiki.get_property_name(member)
        self.assertEqual(txt, "PropName")
    #
    def test_namespace_definition_01(self):
        """ test method: get the class/method name from the attribute. """
        xml_string = '<member name="T:Library.Logger.NamespaceDoc"><summary>The namespace</summary></member>'
        member = ET.fromstring(xml_string)
        ret = self.wiki.namespace_definition(member)
        self.assertEqual(ret, 1)
    #
    def test_class_definition_01(self):
        """ test method: define a class and output it's summary. """
        xml_string = '<member name="T:Config"><summary>Static helpers for handling AppSettings configuration.</summary></member>'
        member = ET.fromstring(xml_string)
        ret = self.wiki.class_definition(member)
        self.assertEqual(ret, 1)
    #
    def test_class_definition_02(self):
        """ test method: define a class and output it's summary. """
        xml_string = """<member name="T:EMail.EMail">
            <summary>
            A fluent interface for smtp mail message
            </summary>
            <remarks>Example: new EMail( from, to, "Subject", "Body").Send()</remarks>
        </member>"""
        member = ET.fromstring(xml_string)
        ret = self.wiki.class_definition(member)
        self.assertEqual(ret, 2)
    #
    def test_class_label_definition_01(self):
        """ test method: get the class/method name from the attribute. """
        xml_string = '<member name="F:Library.ClassName.FieldName"><summary>A field.</summary></member>'
        self.wiki.full_class_name = "Library.ClassName"
        member = ET.fromstring(xml_string)
        ret = self.wiki.class_label_definition(member, 'Flds', 3, 0)
        self.assertEqual(ret, 1)
    #
    def test_class_label_definition_02(self):
        """ test method: get the class/method name from the attribute. """
        xml_string = '<member name="F:Library.ClassName.FieldName"><summary>A field.</summary></member>'
        self.wiki.full_class_name = "Library.ClassName"
        member = ET.fromstring(xml_string)
        ret = self.wiki.class_label_definition(member, 'Flds', 3, 1)
        self.assertEqual(ret, 1)
    #
    def test_class_label_definition_03(self):
        """ test method: get the class/method name from the attribute. """
        xml_string = '<member name="P:Library.ClassName.PropName"><summary>A prop.</summary></member>'
        self.wiki.full_class_name = "Library.ClassName"
        member = ET.fromstring(xml_string)
        ret = self.wiki.class_label_definition(member, 'Props', 3, 0)
        self.assertEqual(ret, 1)
    #
    def test_class_label_definition_04(self):
        """ test method: get the class/method name from the attribute. """
        xml_string = '<member name="P:Library.ClassName.PropName"><summary>A prop.</summary></member>'
        self.wiki.full_class_name = "Library.ClassName"
        member = ET.fromstring(xml_string)
        ret = self.wiki.class_label_definition(member, 'Props', 3, 1)
        self.assertEqual(ret, 1)
    #
    def test_method_definition(self):
        """ test method: define a class and output it's summary. """
        xml_string = '<member name="M:Config"><summary>1</summary><param name="2">2</param><param name="3">3</param><returns>4</returns><exception cref="System.Exception">5</exception></member>'
        member = ET.fromstring(xml_string)
        ret = self.wiki.method_definition(member)
        self.assertEqual(ret, 5)
    #
    def test_return_output_found(self):
        """ test method: for method_return """
        member = ET.fromstring(self.member01)
        ret = self.wiki.return_output(member.find('returns'), 1)
        self.assertEqual(1, ret)
    #
    def test_return_output_empty(self):
        """ test method: for method_return """
        member = ET.fromstring('<returns></returns>')
        ret = self.wiki.return_output(member, 1)
        self.assertEqual(0, ret)
    #
    def test_return_output_para(self):
        """ test method: for method_return """
        member = ET.fromstring('<returns><para>paragraph 1</para></returns>')
        ret = self.wiki.return_output(member, 1)
        self.assertEqual(1, ret)
    #
    def test_method_parameters_not_found(self):
        """ test method: for method_return """
        member = ET.fromstring(self.summary01)
        ret = self.wiki.method_parameters(member)
        self.assertEqual(0, ret)
    #
    def test_method_parameters_found(self):
        """ test method: for method_return """
        member = ET.fromstring(self.member01)
        ret = self.wiki.method_parameters(member)
        self.assertEqual(2, ret)
    #
    def test_exception_output_01(self):
        """ test method: extract and ouput an exception. """
        # <exception cref="System.OverflowException">Thrown.</exception>
        xml_string = '<member name="M:Config"><exception cref="System.OverflowException">Thrown.</exception></member>'
        member = ET.fromstring(xml_string)
        ret = self.wiki.etc_details(member, 4)
        self.assertEqual(ret, 1)
    #
    def test_exception_output_02(self):
        """ test method: extract and ouput an exception. """
        # <member name="P:Library.Logger.Log.Logger">
        #     <summary>
        #     The globally-shared logger.
        #     </summary>
        #     <exception cref="T:System.ArgumentNullException"></exception>
        # </member>
        xml_string = """<member name="P:Library.Logger.Log.Logger">
            <summary>The globally-shared logger.</summary>
            <exception cref="T:System.ArgumentNullException"></exception>
        </member>"""
        member = ET.fromstring(xml_string)
        ret = self.wiki.etc_details(member, 4)
        self.assertEqual(ret, 2)
    #
    def test_lists_bullets(self):
        """ test method: for method_return """
        xml_string = """<example>file 'extent' examples:
            <list type="bullet">
                <item><description>txt</description></item>
                <item><description>tmp</description></item>
                <item><description>log</description></item>
            </list>
        </example>"""
        exam = ET.fromstring(xml_string)
        ret = self.wiki.list_output(exam.find('list'))
        self.assertEqual(3, ret)
    #
    def test_lists_number(self):
        """ test method: for method_return """
        xml_string = """<example>file 'extent' examples:
            <list type="number">
                <item><description>txt</description></item>
                <item><description>tmp</description></item>
                <item><description>log</description></item>
            </list>
        </example>"""
        exam = ET.fromstring(xml_string)
        ret = self.wiki.list_output(exam.find('list'))
        self.assertEqual(3, ret)
    #
    def test_lists_table_01(self):
        """ test method: for method_return """
        xml_string = """<example>file 'extent' examples:
            <list type="table">
                <listheader><term>Extent</term><description>Description</description></listheader>
                <item><term>txt</term><description>text</description></item>
                <item><term>tmp</term><description>temporary</description></item>
                <item><term>log</term><description>log file</description></item>
            </list>
        </example>"""
        exam = ET.fromstring(xml_string)
        ret = self.wiki.etc_output(exam, 4)
        self.assertEqual(5, ret)
        ret = self.wiki.list_output(exam.find('list'))
        self.assertEqual(4, ret)
    #
    def test_lists_table_02(self):
        """ test method: for method_return """
        xml_string = """<example>
            <list type="table">
                <listheader><term></term><description></description></listheader>
                <item><term></term><description></description></item>
                <item><term></term><description></description></item>
            </list>
        </example>"""
        exam = ET.fromstring(xml_string)
        ret = self.wiki.etc_details(exam, 1)
        self.assertEqual(3, ret)
    #
    def test_code_output(self):
        """ test method: ouput an example. """
        xml_string = """<code>
        public void Configuration(IAppBuilder app)
        { ... }
        </code>"""
        elem = ET.fromstring(xml_string)
        ret = self.wiki.code_output(elem)
        self.assertEqual(1, ret)
    #
    def test_etc_details_c(self):
        """ test method: ouput an example. """
        xml_string = """<remarks>paragraph 1<c>in-line code</c>paragraph 1</remarks>"""
        elem = ET.fromstring(xml_string)
        ret = self.wiki.etc_details(elem, 4)
        self.assertEqual(1, ret)
    #
    def test_etc_output_c(self):
        """ test method: ouput an example. """
        xml_string = """<remarks>paragraph 1<c>in-line code</c>paragraph 1</remarks>"""
        elem = ET.fromstring(xml_string)
        ret = self.wiki.etc_output(elem, 4)
        self.assertEqual(2, ret)
    #
    def test_etc_output_remarks_para(self):
        """ test method: ouput a remarks/code/list/example. """
        xml_string = """<remarks><para>paragraph 1</para><para>paragraph 2</para></remarks>"""
        elem = ET.fromstring(xml_string)
        ret = self.wiki.etc_output(elem, 4)
        self.assertEqual(3, ret)
    #
    def test_etc_details(self):
        """ test method: ouput a remarks/code/list/example. """
        xml_string = """<remarks><para>paragraph 1</para><para>paragraph 2</para></remarks>"""
        elem = ET.fromstring(xml_string)
        ret = self.wiki.etc_details(elem, 4)
        self.assertEqual(2, ret)
    #
    def test_etc_details_value_01(self):
        """ test method: get the class/method name from the attribute. """
        xml_string = '<member><summary>Prop Name<value>set/get string prop</value></summary></member>'
        member = ET.fromstring(xml_string)
        ret = self.wiki.etc_details(member, 4)
        self.assertEqual(ret, 2)
    #
    def test_etc_details_value_02(self):
        """ test method: get the class/method name from the attribute. """
        xml_string = """<member><summary>Returns the number of times Counter was called.</summary>
            <value>Number of times Counter was called.</value>
            </member>"""
        member = ET.fromstring(xml_string)
        ret = self.wiki.etc_details(member, 4)
        self.assertEqual(ret, 2)
    #
    def test_etc_details_note_01(self):
        """ test method: get the class/method name from the attribute. """
        xml_string = """<member><note type="note">
         'OrderBy' must be called before the method 'Skip'.
        </note></member>"""
        member = ET.fromstring(xml_string)
        ret = self.wiki.etc_details(member, 4)
        self.assertEqual(ret, 1)
    #
    def test_etc_details_note_02(self):
        """ test method: get the class/method name from the attribute. """
        xml_string = """<member><note type="empty"></note></member>"""
        member = ET.fromstring(xml_string)
        ret = self.wiki.etc_details(member, 4)
        self.assertEqual(ret, 1)
#
if __name__ == '__main__':
    unittest.main()
