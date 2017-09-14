#!/usr/bin/python
#-*- coding: utf-8 -*-


'''

'''
__author__ = 'wpxiao'


class Page(object):

    def __init__(self,user_data,current_page,per_page_row,page_num,base_url):
        '''
            current_page 当前页
            per_page_row 每页显示的条数
            page_num 分页显示的页码数

        '''
        self.user_data = user_data

        self.page_error = ''
        if not current_page.isdigit():
            self.page_error = "页码必须为数字"
            self.current_page = 1
        else:
            self.current_page = int(current_page)
        self.per_page_row = int(per_page_row)
        self.page_num = int(page_num)
        self.base_url = base_url


    #数据的总页数
    @property
    def total_page(self):
        total_page, mod = divmod(len(self.user_data), self.per_page_row)
        if mod != 0:
            total_page = total_page + 1

        if self.current_page > total_page:
            self.page_error = "页码超出范围"
            self.current_page = 1

        return total_page

    #分页显示时当前页面的第一条数
    @property
    def start(self):
        start = (self.current_page - 1) * self.per_page_row
        return start

    #分页显示时当前页面的最后一条数据
    @property
    def end(self):
        end = self.current_page * self.per_page_row
        return end

    def page_str(self):
        '''
            分页逻辑：
            当总页数大于等于11时
                如果当前页 小于等于6时
                    开始页 = 1
                    结束页 = 11 +1
                如果当前页 大于6时
                    开始页 = 当前页 - 5
                    如果当前页+5 > 总页数
                        结束页 = 总页数 +1
                    否则
                        结束页 = 当前页 + 5+1
            当总页数小于11时,
                开始页 = 1
                结束页 = 总页数+1
        '''
        if self.total_page < self.page_num:
            start_page = 1
            end_page = self.total_page + 1
        else:
            if self.current_page <= (self.page_num + 1) / 2:
                start_page = 1
                end_page = self.page_num + 1
            else:
                start_page = int(self.current_page - (self.page_num - 1) / 2)
                if self.current_page + (self.page_num - 1) / 2 > self.total_page:
                    end_page = self.total_page + 1
                else:
                    end_page = int(self.current_page + (self.page_num + 1) / 2)

        page_list = []
        if self.current_page == 1:
            a_tag = '''
                            <a class="selected" href="javascript:void(0)">上一页</a>
                    '''
        else:
            a_tag = '''
                            <a class="selected" href="%s?p=%s">上一页</a>
                    ''' % (self.base_url,self.current_page - 1,)
        page_list.append(a_tag)

        for i in range(start_page, end_page):
            if i < 10:
                i_text = "0" + str(i)
            else:
                i_text = str(i)
            if self.current_page == i:
                a_tag = '''
                    <a class="selected" href="%s?p=%s">%s</a>
                ''' % (self.base_url,i, i_text)
            else:
                a_tag = '''
                    <a href="%s?p=%s">%s</a>
                ''' % (self.base_url,i, i_text)
            page_list.append(a_tag)

        if self.current_page == self.total_page:
            a_tag = '''
                            <a class="selected" href="javascript:void(0)">下一页</a>
                    '''
        else:
            a_tag = '''
                            <a class="selected" href="%s?p=%s">下一页</a>
                    ''' % (self.base_url,self.current_page + 1,)
        page_list.append(a_tag)

        input_tag = '''
            <input  size='5px' id="jump_page" type="text" name="jump_page" placeholder='页码' />
            <input type="button" id="jump_btn" onclick="JumpTo(this,'%s?p=');" value="GO" />
            <script>
                function JumpTo(ths,base_url){
                    var val = ths.previousElementSibling.value;
                    location.href = base_url+ val; 
                }
            </script>
        '''%(self.base_url,)
        page_list.append(input_tag)

        page_list = "".join(page_list)
        return page_list

if __name__ == "__main__":
    p = Page([1,2,3,4,5,6],'2','2','10')
    print(p.page_str())