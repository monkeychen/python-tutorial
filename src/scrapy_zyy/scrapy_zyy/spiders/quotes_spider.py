import scrapy
from urllib import parse as url_parse

from ..items import ScrapyZyyItem


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    cks = 'JSESSIONID=BEAE1D1CABF3B16BD38B7BEA41465034; Hm_lvt_bcdd6b6a2ae8dea180ab872d11287b7e=1601457160; languageFile=zh_CN'
    opt_label_dict = {
        'exama': '选项A', 'examb': '选项B', 'examc': '选项C', 'examd': '选项D',
        'exame': '选项E', 'examf': '选项F', 'examg': '选项G', 'examh': '选项H',
        'exami': '选项I', 'examj': '选项J', 'examk': '选项K', 'examl': '选项L'
    }

    def start_requests(self):
        tmp = 'http://net.chinamobile.com/exam/web/exam/examInfoListActionCreateDraftAuditList.action?type=3&pageNum='
        urls = [tmp + str(i) for i in range(1, 29)]

        cookies = {i.split('=')[0]: i.split('=')[1] for i in self.cks.split('; ')}
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, cookies=cookies)

    def parse(self, response):
        cookies = {i.split('=')[0]: i.split('=')[1] for i in self.cks.split('; ')}
        q_urls = response.xpath('//*[@id="user_form"]/table/tr/td/a/@href').extract()
        print('\n'.join(q_urls))
        for url in q_urls:
            yield scrapy.Request(url=url, callback=self.parse_question, cookies=cookies)

    def parse_question(self, response):
        # url_query_dic = url_parse.parse_qs(url_parse.urlparse(response.url).query)
        # q_id = url_query_dic['id'][0]
        # filename = 'question-%s.txt' % q_id
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        content = response.xpath('//*[@id="content"]/text()')[0].extract()
        input_ele_list = response.xpath('//*[@id="examform"]/table/tr/td[2]/input')
        option_str = ''
        ans_str = ''
        q_type = '多选题'
        for input_ele in input_ele_list:
            type_val = input_ele.xpath('@type').extract_first()
            name = input_ele.xpath('@name').extract_first()
            val = input_ele.xpath('@value').extract_first()
            if type_val == 'radio' and name == 'exam.type':
                checked = input_ele.xpath('@checked').extract_first()
                if checked == 'checked':
                    q_type = '单选题' if val == '0' else '多选题'
            elif type_val == 'text':
                q_id = input_ele.xpath('@id').extract_first()
                option_str = option_str + self.opt_label_dict[q_id] + "：" + val + "，"

        single_ans_list = response.xpath('//*[@id="reultDiv1"]/input')
        multi_ans_list = response.xpath('//*[@id="reultDiv2"]/input')
        ans_input_list = single_ans_list if q_type == '单选题' else multi_ans_list
        for ans_input in ans_input_list:
            ans_val = ans_input.xpath('@value').extract_first()
            ans_checked = ans_input.xpath('@checked').extract_first()
            if ans_checked == 'checked':
                ans_str = ans_str + '' + ans_val

        line = ('题型：%s | 试题内容：%s | 答案：%s | %s' % (q_type, content, ans_str, option_str)) + "\n"
        item = ScrapyZyyItem()
        item['line'] = line
        yield item

        # with open('question-all.txt', 'a') as f2:
        #     f2.write(line)

        # self.log('Saved file %s' % filename)

