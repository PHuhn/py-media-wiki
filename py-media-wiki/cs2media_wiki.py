""" module: Convert from .Net meta comments to Media Wiki """
import sys as Sys
import io as IO
from defusedxml.ElementTree import parse
from pathlib import Path
# Variable
# .0 Initial commit
# .1 Improved code output
# .2 value tag handled
# .3 ``1 to <T>
VERSION = "1.0.5"
# ============================================================================
class CS2MediaWiki():
    """ class: Convert from .Net meta comments to Media Wiki
        the following are the available tags:
        <c>           <para>         <see>*
        <code>        <param>*       <seealso>*
        <example>     <paramref>     <summary>
        <exception>*  <permission>*  <typeparam>*
        <include>*    <remarks>      <typeparamref>
        <list>        <returns>      <value>
        Member types
        N: namespace
        T: type: class, interface, struct, enum, delegate
        F: field
        P: property
        M: method
        E: event
        !: error string

        not handled
        * see,      ignored
        * seealso,  ignored
        * typeparam
        * paramref
        * typeparamref
        * include
        * permission
        * E: event
        * !: error string
    """
    name_space = ''
    class_name = ''
    full_class_name = ''
    err_label = "~~~~~~ Error: "
    ctor_flg = 0
    mthd_flg = 0
    wiki_header = '='
    wiki_hr = '----'
    wiki_italic = "''"
    wiki_bold = "'''"
    wiki_list_bullet = '*'
    wiki_list_number = '#'
    wiki_table_start = '{|'
    wiki_table_end = '|}'
    wiki_table_hstart = '!'
    wiki_table_hcell = '!!'
    wiki_table_istart = '|'
    wiki_table_icell = '||'
    wiki_code_start = '<source lang="csharp">'
    wiki_code_end = '</source>'
    wiki_inlinecode_start = '<code>'
    wiki_inlinecode_end = '</code>'
    #
    # ========================================================================
    # wiki specific methods:
    # * header
    # * italic_text
    # * bold_text
    # * list_output
    # * code_output
    #
    def header(self, text, level):
        """ method: process child assembly, making it a level 1 header. """
        if level < 1:
            level = 1
        if level > 6:
            level = 6
        return "{0} {1} {0}".format((level * self.wiki_header), text)
    #
    def italic_text(self, text):
        """ method: return the text with italic markup. """
        return "{0}{1}{0}".format(self.wiki_italic, text)
    #
    def bold_text(self, text):
        """ method: return the text with bold markup. """
        return "{0}{1}{0}".format(self.wiki_bold, text)
    #
    def text_left_trim(self, text):
        if text == "":
            return text
        if text[0] == '\n':
            text = text.lstrip('\n')
        handle = IO.StringIO(text)
        ret_text = ""
        for line in handle:
            ret_text += line.lstrip()
        return ret_text.rstrip('\n')
    #
    def text_left_trunc(self, text, minus):
        if text == "":
            return text
        if text[0] == '\n':
            text = text.lstrip('\n')
        handle = IO.StringIO(text)
        ret_text = ""
        wsp_len = len(text) - (len(text.lstrip()) + minus)
        whsp = " " * wsp_len
        if wsp_len > 0:
            for line in handle:
                if whsp == line[:wsp_len]:
                    ret_text += line[wsp_len:]
        else:
            ret_text = text
        return ret_text.rstrip('\n')
    #
    def get_element_text(self, element):
        """ method: recusively get an element's text.
        see: stackoverflow.com how-do-i-get-the-full-xml-or-html-content-of-an-element-using-elementtree
        """
        text = element.text or ''
        for subelement in element:
            if (subelement.tag == "see") or (subelement.tag == "seealso"):
                text += self.get_element_text(subelement)
        text += element.tail or ''
        return self.text_left_trim(text)
    #
    def root(self, root):
        """ method: process child assembly, making it a level 1 header. """
        # <?xml version="1.0"?>
        # <doc>
        #     <assembly>
        #         <name>Library.Helpers</name>
        #     </assembly>
        #     ...
        # </doc>
        prop_flg = 0
        fld_flg = 0
        ret = 0
        for child in root:
            if child.tag == 'assembly':
                self.name_space = self.assembly_name(child)
                ret += 1
            if child.tag == 'members':
                for member in child:
                    # member {'name': 'T:Library.Helpers.NamespaceDoc'}
                    att = member.attrib.get('name')
                    if att[:2] == "T:":
                        if att[-12:] == "NamespaceDoc":
                            self.namespace_definition(member)
                        else:
                            self.class_definition(member)
                            prop_flg = 0
                            fld_flg = 0
                            self.ctor_flg = 0
                            self.mthd_flg = 0
                        ret += 1
                    elif att[:2] == "M:":
                        self.method_definition(member)
                        ret += 1
                    elif att[:2] == "F:":
                        self.class_label_definition(member, 'Fields', 3, fld_flg)
                        fld_flg += 1
                        ret += 1
                    elif att[:2] == "P:":
                        self.class_label_definition(member, 'Properties', 3, prop_flg)
                        prop_flg += 1
                        ret += 1
                    else:
                        print(self.err_label, "unknown attribute:", att)
        return ret
    #
    def assembly_name(self, child_assembly):
        """ method: process child assembly, making it a level 1 header.
        """
        # <assembly>
        #  <name>Library.Logger</name>
        # </assembly>
        ret = 'unknown'
        for assm in child_assembly:
            if assm.tag == 'name':
                ret = assm.text
        print(self.header("Assembly: {0}".format(ret), 1))
        return ret
    #
    def get_member_attrib_name(self, member):
        """ method: get the class/method name from the attribute. """
        # <member name="M:Library.Helpers.Config.GetStringAppSettingConfigValue(System.String,System.String)">
        member_name = member.attrib.get('name')[2:]
        ns_len = len(self.name_space)
        if ns_len > 0:
            if ns_len != len(member_name):
                if self.name_space == member_name[:ns_len]:
                    member_name = member_name[ns_len + 1:]
        return member_name
    #
    def get_property_name(self, member):
        """ method: get the class/method name from the attribute. """
        # <member name="M:Library.Helpers.Config.GetStringAppSettingConfigValue(System.String,System.String)">
        member_name = member.attrib.get('name')[2:]
        cls_len = len(self.full_class_name)
        if cls_len > 0:
            if self.full_class_name == member_name[:cls_len]:
                member_name = member_name[cls_len + 1:]
        return member_name
    #
    def namespace_definition(self, member):
        """ method: define a namespace and output it's summary. """
        # <member name="T:Library.Logger.NamespaceDoc">
        #     <summary>
        #     The <see cref="N:Library.Logger"/> namespace contains classes ...
        #     </summary>
        # </member>
        name = member.attrib.get('name')[2:]
        nm_len = len(name)
        name = name[0:nm_len - 13]
        self.name_space = name
        print(self.header("Namespace: {0}".format(name), 1))
        ret = self.etc_details(member, 2) # summary description
        return ret
    #
    def class_definition(self, member):
        """ method: define a class and output it's summary.
        """
        # <member name="T:Library.Helpers.Config">
        #     <summary>
        #     Static helpers for handling AppSettings configuration.
        #     </summary>
        # </member>
        self.class_name = self.get_member_attrib_name(member)
        self.full_class_name = member.attrib.get('name')[2:]
        print(self.header("Class: {0}".format(self.class_name), 2))
        ret = 0
        ret += self.etc_details(member, 3) # summary description
        print("\n\n{0}\n\n".format(self.wiki_hr))
        return ret
    #
    def class_label_definition(self, member, label, level, flag):
        """ method: define a header of field or property definition. """
        # <member name="F:Library.EMail.EMail.Logging">
        #     <summary>
        #     This is an implementation of ILogging.  Errors are loggged
        #     to the ILogger during the sending of email.
        #     </summary>
        # </member>
        var_name = self.get_property_name(member)
        if flag == 0:
            print(self.header(label, level))
        print(self.header(var_name, level + 1))
        ret = 0
        ret += self.etc_details(member, level + 2) # summary description
        # print("\n\n{0}\n\n".format(self.wiki_hr))
        return ret
    #
    def get_param_names(self, member):
        """ method: get all parameter names and store in an array """
        p_names = []
        p_names.append("")  # zeroth (the method name)
        for param in member:
            if (param.tag == 'param') or (param.tag == 'typeparam'):
                p_names.append(param.get('name'))
        return p_names
    #
    def reconstruct_method(self, member, method_name):
        """ method: reconstruct the method
        dealing with the following:
         IQueryable<T> LazyOrderBy<T>(this IQueryable<T> qry, LazyLoadEvent lle)
        """
        p_names = self.get_param_names(member)
        fnd = method_name.find("``")
        while fnd > -1:
            indx = int(method_name[fnd + 2])
            if method_name[fnd-1] == "{":
                if indx == 0:
                    t_type = "&lt;" + p_names[1] + "&gt;"
                    method_name = method_name[:fnd-1] + t_type + method_name[fnd + 4:]
                else:
                    return method_name
            else:
                t_type = "&lt;" + p_names[indx] + "&gt;"
                method_name = method_name[:fnd] + t_type + method_name[fnd + 3:]
            fnd = method_name.find("``")
        #
        return method_name
    #
    def cleanup_system_method(self, method_name):
        """ method: reconstruct the method
        dealing with the following:
            <member name="M:MimeKit.Extensions.From(MimeKit.MimeMessage,System.String,System.String)">
        to:
            From(MimeKit.MimeMessage, String, String)
        """
        method_name = method_name.replace(",System.", ", ").replace("(System.", "(").replace("," + self.name_space + ".", ", ").replace("(" + self.name_space + ".", "(")
        return method_name
    #
    def method_definition(self, member):
        """ method: extract and ouput a members summary.
        """
        # <member name="M:Library.Helpers.Config.GetStringAppSettingConfigValue(System.String,System.String)">
        #     <summary>
        #     Get a value from the AppSetting section of the web config.
        #     </summary>
        #     <param name="configAppKey">AppSetting key value</param>
        #     <param name="defaultValue">if not found return this value</param>
        #     <returns>string of the value in the appSetting section in the config file.</returns>
        # </member>
        method_name = self.get_property_name(member)
        if method_name[-1:] != ")":
            method_name = method_name + "()"
        if method_name[:5] == "#ctor":
            method_name = self.class_name + method_name[5:]
            if self.ctor_flg == 0:
                print(self.header("Constructors", 3))
            self.ctor_flg += 1
        else:
            if self.mthd_flg == 0:
                print(self.header("Methods", 3))
            self.mthd_flg += 1
        method_name = self.reconstruct_method(member, method_name)
        method_name = self.cleanup_system_method(method_name)
        print(self.header(method_name, 4))
        ret = self.etc_details(member, 5) # summary description
        ret += self.method_parameters(member)
        print("\n\n{0}\n\n".format(self.wiki_hr))
        return ret
    #
    def method_parameters(self, member):
        """ method: extract and ouput all method parameters. """
        # <param name="fullFilePathAndName">full path and file name</param>
        count = 0
        for param in member:
            if (param.tag == 'param') or (param.tag == 'typeparam'):
                count += 1
                if count == 1:
                    print(self.header("Parameters", 5))
                print(self.header(param.get('name'), 6))
                print(self.get_element_text(param))
                count += self.etc_details(param, 6) # summary description
            elif param.tag == 'returns':
                count += self.return_output(param, 5)
        return count
    #
    def exception_output(self, excpt, level):
        """ method: extract and ouput a method's return. """
        # <exception cref="System.OverflowException">Thrown when one parameter is max
        # and the other is greater than 0.</exception>
        count = 0
        if excpt.tag == 'exception':
            val = excpt.text
            exception_name = excpt.attrib.get('cref')
            if (val is None) and (exception_name is None):
                print(self.err_label, "Empty return value")
            else:
                if exception_name[:2] == "T:":
                    exception_name = exception_name[2:]
                print(self.header(exception_name, level))
                if val is not None:
                    print(val.lstrip())
                count = 1
        return count
    #
    def return_output(self, ret_elem, level):
        """ method: extract and ouput a method's return. """
        # <returns>string of prefix followed by GUID and extent</returns>
        count = 0
        if ret_elem.tag == 'returns':
            val = self.get_element_text(ret_elem)
            print(self.header("Return Value", level))
            print(val.lstrip())
            if val != "":
                count = 1
            count += self.etc_details(ret_elem, level + 1)
            if count == 0:
                print(self.err_label, "Empty return value")
        return count
    #
    def list_output(self, list_tag):
        """ method: ouput a bulleted/number list or table. """
        # <list type="bullet" | "number" | "table">
        #     <listheader>
        #         <term>term</term>
        #         <description>description</description>
        #     </listheader>
        #     <item>
        #         <term>term</term>
        #         <description>description</description>
        #     </item>
        # </list>
        count = 0
        if list_tag.tag == 'list':
            l_type = list_tag.get('type')
            if l_type == "bullet":
                list_type = self.wiki_list_bullet
            else:
                if l_type == "number":
                    list_type = self.wiki_list_number
                else:
                    list_type = "T"
                    print(self.wiki_table_start)
            for item in list_tag:
                count += 1
                term = ""
                descr = ""
                if item.find("./term") is not None:
                    term = item.find("./term").text or ""
                if item.find("./description") is not None:
                    descr = item.find("./description").text or ""
                if list_type == "T":
                    if item.tag == "listheader":
                        print("{0}{1}{2}{3}".format(self.wiki_table_hstart, self.bold_text(term),
                                                    self.wiki_table_hcell, self.bold_text(descr)))
                    else:
                        print("{0}{1}{2}{3}".format(self.wiki_table_istart, term,
                                                    self.wiki_table_icell, descr))
                else:
                    print("{0} {1} {2}".format(list_type, term, descr))
            if list_type == "T":
                print(self.wiki_table_end)
            print("")
        return count
    #
    def c_output(self, elem):
        """ method: ouput an example. """
        # <c>System.Exception</c>
        ret = 0
        if elem.tag == 'c':
            print("{0}{1}\n{2}".format(self.wiki_inlinecode_start, elem.text, self.wiki_inlinecode_end))
            ret = 1
        return ret
    #
    def code_output(self, elem):
        """ method: ouput an example. """
        # <code>
        # public void Configuration(IAppBuilder app)
        # {
        #     ...
        # }
        # </code>
        ret = 0
        if elem.tag == 'code':
            print(self.wiki_code_start)
            print(self.text_left_trunc(elem.text, 0))
            print(self.wiki_code_end)
            ret = 1
        return ret
    #
    def bold_label_text(self, label, text):
        """ method: ouput a note/example/remark. """
        return "{0} {1}".format(self.bold_text(label), text)
    #
    def bold_label_output(self, label, text):
        """ method: ouput a note/example/remark. """
        print("\n{0}".format(self.bold_label_text(label, text)))
        return 1
    #
    def note_output(self, note_elem, level):
        """ method: ouput a note. """
        # <note type="note">
        #  'OrderBy' must be called before the method 'Skip'.
        # </note>
        count = 0
        if note_elem.tag == 'note':
            n_type = note_elem.get('type')
            n_type = n_type[0].upper() + n_type[1:]
            text = self.get_element_text(note_elem)
            self.bold_label_output(n_type + ":", text)
            count += 1 + self.etc_details(note_elem, level)
        return count
    #
    # summary/remark/example/code/list
    def etc_output(self, detail, level):
        """ method: ouput a summary/remark/code/list/example. """
        ret = 0
        detail_tag = detail.tag
        if detail_tag == 'summary':
            # <summary>
            # The <see cref="N:Library.Helpers"/> namespace contains a
            # collection of static helper methods.
            # </summary>
            # elem_text = detail.text.lstrip() + detail.tail
            elem_text = self.get_element_text(detail)
            print(elem_text)
            ret += 1 + self.etc_details(detail, level)
        elif detail_tag == 'returns':
            ret += self.return_output(detail, level)
            # to etc_details handled in return_output
        elif detail_tag == 'exception':
            ret += self.exception_output(detail, level)
            ret += self.etc_details(detail, level + 1)
        elif detail_tag == "remarks":
            # <remarks>Example: new EMail( from, to, "Subject", "Body").Send()</remarks>
            text = self.get_element_text(detail)
            self.bold_label_output("Remarks:", text)
            ret += 1 + self.etc_details(detail, level)
        elif detail_tag == "example":
            # <example>
            # This sample shows how to call this constructor.
            # <code> ... </code>
            # </example>
            text = self.get_element_text(detail)
            self.bold_label_output("For example:", text)
            ret += 1 + self.etc_details(detail, level)
        elif detail_tag == "para":
            # <remark><para>paragraph 1</para><para>paragraph 2</para></remark>
            print(self.get_element_text(detail))
            ret += 1 + self.etc_details(detail, level)
        elif detail_tag == "c":
            ret += self.c_output(detail)
        elif detail_tag == "code":
            ret += self.code_output(detail)
        elif detail_tag == "list":
            ret += self.list_output(detail)
        elif detail_tag == 'value':
            # <value>property-description</value>
            elem_text = self.get_element_text(detail)
            print(self.italic_text(elem_text))
            ret += 1 + self.etc_details(detail, level)
        elif detail_tag == 'note':
            ret += self.note_output(detail, level)
        else:
            print(self.err_label, "unknown tag:", detail_tag)
        #
        return ret
    # remark/code/list/example
    def etc_details(self, details, level):
        """ method: ouput a remark/code/list/example. """
        ret = 0
        for detail in details:
            detail_tag = detail.tag
            if detail_tag in ("summary", "exception", "remarks", "example", "para", "c", "code", 'value', 'note'):
                ret += self.etc_output(detail, level)
            elif detail_tag in ("param", "typeparam", "returns"):
                pass    # handled and grouped in method_definition
            elif detail_tag  in ("see", "seealso"):
                pass    # ignore these, of no service in wiki
            elif detail_tag == "list":
                ret += self.list_output(detail)
            else:
                print(self.err_label, "unknown tag:", detail_tag)
        return ret
#
if __name__ == '__main__':
    #
    WIKI = CS2MediaWiki()
    USAGE = "\nVersion {0}\n\nUsage: {1} <XML file>".format(VERSION, Sys.argv[0])
    ARGC = len(Sys.argv)
    FILE = "" # "./data/Library.Email.xml"
    if ARGC == 2:
        if Sys.argv[1][0] == '-':
            print(USAGE)
            exit(0)
        FILE = Sys.argv[1]
    else:
        print(USAGE)
        exit(0)
    if FILE != "":
        INPUT_FILE = Path(FILE)
        if INPUT_FILE.exists():
            ET = parse(FILE)
            ROOT = ET.getroot()
            if ROOT.tag == 'doc':
                WIKI.root(ROOT)
            else:
                print("Invalid root type, must be 'doc', file: " + FILE)
        else:
            print("File: " + FILE + ", does not exist")
    else:
        print("File required.")
