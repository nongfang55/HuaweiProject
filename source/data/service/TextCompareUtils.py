# coding=gbk
from source.utils.pandas.pandasHelper import pandasHelper
import re


class TextCompareUtils:
    """patch���ı��Ƚ���"""

    @staticmethod
    def patchParser(text):
        """patch���ı�����"""

        """ patch �ı���ʽʾ��˵��
        
         @@ -35,9 +36,8 @@ ruby <%= \"'#{RUBY_VERSION}'\" -%>
         # gem 'rack-cors'
         
         <%- end -%>
         -# The gems below are used in development, but if they cause problems it's OK to remove them
         -
         <% if RUBY_ENGINE == 'ruby' -%>
         +# The gems below are used in development, but if they cause problems it's OK to remove them
         group :development, :test do
         # Call 'byebug' anywhere in the code to stop execution and get a debugger console
         gem 'byebug', platforms: [:mri, :mingw, :x64_mingw]
         
         
         ˵����  -35,9,+36,8  ˵������Ķ����ϸ��汾��35�п�ʼ��������9����ԭ���汾������
                                           �¸��汾36�п�ʼ������8�����°汾������
                                           "+" �����°汾���е�����
                                           "-" �����ϰ汾���е�����
                                           
                patch �ĵ�һ�в�������
        ע�� �������Լ���������� @���ݷ�
        """

        changes = []  # һ��patch���ܻ��ж���Ķ�    [(��ʼ��,��,�汾����ʼ,��) -> [+, ,-,....]]
        # print(text)
        # print('-' * 50)

        headMatch = re.compile(r'@@(.)+@@')
        numberMatch = re.compile(r'[^0-9]+')

        status = None
        lines = []
        for t in text.split('\n'):
            """���в��  ���ν���"""
            head = headMatch.search(t)
            if head:
                if status is not None:
                    changes.append([status, lines])
                    status = None
                    lines = []

                print(head.group())
                numbers = [int(x) for x in numberMatch.split(head.group()) if x.__len__() > 0]
                print(numbers)
                if numbers.__len__() == 4:
                    status = tuple(numbers)
                elif numbers.__len__() == 2:
                    """������ֻ���������������"""
                    numbers = (numbers[0], 1, numbers[1], 1)
                    status = numbers
            else:
                """�ռ��������� ��ÿһ���޸�״̬"""
                if t.__len__() > 0:
                    lines.append(t[0])
        if status is not None:
            changes.append([status, lines])
        # print(changes)
        return changes

    @staticmethod
    def simulateTextChanges(patches1, patches2, targetLine):
        """ͨ����patch���ı�ģ������ñ仯�����
          ��Patch1 �ĸĶ�����ģ��
          ��Patch2 �ĸĶ�����ģ��

        """

        changes1 = []
        changes2 = []

        # minLine = float('inf')
        maxLine = 0  # ��ʡ�ռ��ѯ�漰�仯���Ͻ���
        for patch in patches1:
            change = TextCompareUtils.patchParser(patch)  # ÿһ��patch�����м����仯����ƽ�й�ϵ
            changes1.insert(0, change)

            for c in change:
                # minLine = min(minLine, c[0])
                """���޸ı��Ŀ��ܻ��漰��������� �����ı�ģ��ĸ���"""
                maxLine = max(maxLine, c[0][0] + c[1].__len__(), c[0][2] + c[1].__len__())
        for patch in patches2:
            change = TextCompareUtils.patchParser(patch)
            changes2.insert(0, change)
            for c in change:
                # minLine = min(minLine, c[0])
                maxLine = max(maxLine, c[0][0] + c[1].__len__(), c[0][2] + c[1].__len__())

        maxLine = max(maxLine + 20, targetLine + 20)
        print(maxLine)

        """ͨ��һ��������ģ���ı��ı仯"""
        text = [x for x in range(1, maxLine)]  # ����ģ���ı�
        print(text)

        """����ģ����� һ������ �����е����ִ����к�  ���������ʹ��Patch������"""

        """���ڷ���·��������  ���Ķ��м�����Ϊ������   ������Ϊ������"""
        for changes in changes1:
            """����ģ��ʱ�������ƫ��"""
            offset = 0
            for change in changes:
                cur = change[0][2] - offset
                print('start  offset:', change[0], offset)
                for c in change[1]:
                    if c == ' ':
                        cur += 1
                    elif c == '-':
                        text.insert(cur - 1, 0)
                        cur += 1
                    elif c == '+':
                        text.pop(cur - 1)
                """ɾ���е���ԭ������ʼ������λ  ��Ҫ����ƫ�Ʋ���"""

                """����ƫ��δ�ۼӵ��µ�bug"""
                offset += change[1].count('+') - change[1].count('-')

        """ǰ��·��Ϊ��"""
        for changes in changes2:
            offset = 0
            for change in changes:
                cur = change[0][0] + offset
                print('start  offset:', change[0], offset)
                for c in change[1]:
                    if c == ' ':
                        cur += 1
                    elif c == '+':
                        text.insert(cur - 1, 0)
                        cur += 1
                    elif c == '-':
                        text.pop(cur - 1)
                offset += change[1].count('+') - change[1].count('-')
        print(text)
        return text

    @staticmethod
    def getClosedFileChange(patches1, patches2, commentLine):
        """���ĳ�����������line   �������ʮ�򷵻�-1  patch��˳���ǴӸ�������"""

        text = TextCompareUtils.simulateTextChanges(patches1, patches2, commentLine)

        """text��ģ��commit����֮����ı�"""

        if commentLine not in text:
            """�����в��� �仯֮����ı����У�˵�����б仯������0"""
            return 0
        else:
            """Ѱ�Ҿ���Ʒ������ĸĶ�����"""
            curLine = text.index(commentLine)

            """������������� ����0�������"""
            upChange = None
            downChange = None
            for i in range(1, min(11, curLine)):
                """���ִ�λ��������Ϊ0���ı�Ϊֹ"""
                if text[curLine - i] != commentLine - i:
                    upChange = i
                    break
            for i in range(1, min(11, text.__len__() - curLine)):
                if text[curLine + i] != commentLine + i:
                    downChange = i
                    break

            """-1��ʾ����û�иĶ�"""
            if upChange is None and downChange is None:
                return -1

            if downChange is None:
                return upChange
            elif upChange is None:
                return downChange
            else:
                return min(upChange, downChange)

    @staticmethod
    def getStartLine(text, originalPosition):
        """ͨ���ı�originalPosition���ƶϳ�
           review comment��original_StartLine �� side

           ע�� 2020.7.9 ���� position �Ǵ�ָ����commit����λ�ã�
        """

        """patch ����"""
        """��Ȼ patch ���ܻ������� �������ݿ�14��comment ֻ��37���������
           ����try catch�����������
        """
        side = None
        original_startLine = None
        try:
            changes = TextCompareUtils.patchParser(text)
            """�ҵ���Ӧ�ĸĶ�"""
            """��һ�в�����"""
            originalPosition += 1
            pos = 0
            posLine = 0
            while posLine + changes[pos][1]. __len__() + 1 < originalPosition:
                posLine += changes[pos][1].__len__() + 1
                pos += 1

            original_startLine = None
            side = None
            left_start, _, right_start, _ = changes[pos][0]
            status = changes[pos][1]
            if originalPosition is not None:
                if status[originalPosition - posLine - 2] == '-':
                    side = 'LEFT'
                    original_startLine = left_start
                else:
                    side = 'RIGHT'
                    original_startLine = right_start
                offset = 0
                if side == 'LEFT':
                    for i in range(0, max(originalPosition - posLine - 1, 0)):
                        if status[i] != '+':
                            offset += 1
                if side == 'RIGHT':
                    for i in range(0, max(originalPosition - posLine - 1, 0)):
                        if status[i] != '-':
                            offset += 1
                original_startLine = original_startLine + offset - 1
        except Exception as e:
            print(e)

        return original_startLine, side

    @staticmethod
    def ConvertLeftToRight(text, originalPosition):
        """���� comment ���ܻ����  �ϰ汾(LEFT) ���°汾 (RIGHT)����
        ���棬�ϰ汾���������°汾������������ͬ�� ����comment��chnage��
        �汾�Ƚ϶���   ���°汾��RIGHT�� ��  change �汾�ıȽϣ���Ҫ��
        LEFT������ ת��Ϊ �����RIGHT ����

           ע�� 2020.7.9 ֮ͬǰ��ͬ����Patch�ɶ��Сpatch��ɵ�ʱ��
           ����ƴ�ӳ������ܻ���1�����ҵ����  ���ԭ����
           ����LEFT �� comment ��ԱȽ��� ��LEFT:RIGHT = 1 �� 10��
           ��ת���鿴Ч��
        """
        try:
            changes = TextCompareUtils.patchParser(text)
            """�ҵ���Ӧ�ĸĶ�"""
            """��һ�в�����"""
            originalPosition += 1
            pos = 0
            posLine = 0
            while posLine + changes[pos][1]. __len__() + 1 < originalPosition:
                posLine += changes[pos][1].__len__() + 1
                pos += 1

            left_start, _, right_start, _ = changes[pos][0]
            status = changes[pos][1]
            if originalPosition is not None:
                """�϶����õ�comment����LEFT"""
                offset = 0
                for i in range(0, max(originalPosition - posLine - 1, 0)):
                    """ͳ�� RIGHT �汾�е�����"""
                    if status[i] != '-':
                        offset += 1

                return right_start + offset - 1
        except Exception as e:
            print(e)

        return None


if __name__ == '__main__':
    # data = pandasHelper.readTSVFile(r'C:\Users\ThinkPad\Desktop\select____from_gitCommit_gitFile__where_.tsv',
    #                                 pandasHelper.INT_READ_FILE_WITHOUT_HEAD)
    # text = data.as_matrix()[0][18]
    # print(TextCompareUtils.patchParser(text))
    # print(text)
    # for t in text.split('\n'):
    #     print(t)
    #text = "@@ -20,6 +20,7 @@ ruby <%= \"'#{RUBY_VERSION}'\" -%>\n <% end -%>\n <% end -%>\n \n+\n # Optional gems needed by specific Rails features:\n \n # Use bcrypt to encrypt passwords securely. Works with https://guides.rubyonrails.org/active_model_basics.html#securepassword\n@@ -35,9 +36,8 @@ ruby <%= \"'#{RUBY_VERSION}'\" -%>\n # gem 'rack-cors'\n \n <%- end -%>\n-# The gems below are used in development, but if they cause problems it's OK to remove them\n-\n <% if RUBY_ENGINE == 'ruby' -%>\n+# The gems below are used in development, but if they cause problems it's OK to remove them\n group :development, :test do\n   # Call 'byebug' anywhere in the code to stop execution and get a debugger console\n   gem 'byebug', platforms: [:mri, :mingw, :x64_mingw]\n@@ -75,7 +75,6 @@ group :test do\n   # Easy installation and use of web drivers to run system tests with browsers\n   gem 'webdrivers'\n end\n-\n <%- end -%>\n \n <% if depend_on_bootsnap? -%>"
    #text = "@@ -2,9 +2,9 @@ a\n b\n c\n d\n-e\n a\n b\n+aa\n c\n d\n a\n@@ -123,10 +123,8 @@ a\n d\n f\n d\n-\n+aaa\n t\n-ty\n-u\n u\n u\n y\n@@ -233,10 +231,10 @@ ter\n t\n t\n d\n-\n+zzzz\n t\n-rt\n-ert\n+zz\n+erzt\n r\n t\n rt"
    text = """@@ -47,4 +47,13 @@ let () =
     args
     (fun s -> raise (Arg.Bad (Format.sprintf "Unexpected argument: %s" s)))
     usage_msg ;
-  Stdlib.exit (Lwt_main.run @@ Validator.main ?socket_dir:!socket_dir ())
+  let main_promise = Validator.main ?socket_dir:!socket_dir () in
+  Stdlib.exit
+    (Lwt_main.run
+       ( Lwt_exit.wrap_and_exit main_promise
+       >>= function
+       | Ok () ->
+           Lwt_exit.exit_and_wait 0
+       | Error err ->
+           Format.eprintf "%a\n%!" pp_print_error err ;
+           Lwt_exit.exit_and_wait 1 ))
"""
    text = text.replace("\\", "")
    print(TextCompareUtils.patchParser(fr"{text}"))
    # print(TextCompareUtils.ConvertLeftToRight(text, 33))
