import scrapy
from datetime import datetime
from dateutil.rrule import *
from dateutil.parser import parse

url = 'http://www2.bmf.com.br/pages/portal/bmfbovespa/lumis/lum-resumo-operacoes-ptBR.asp'

class DerivativesVolumeSpider(scrapy.Spider):
    name = 'volume_spider'

    def start_requests(self):
        dates = date_range("01/01/2021",datetime.today().strftime("%d/%m/%Y"))

        for date in dates:
            yield scrapy.FormRequest(url,formdata={"dData1": date},meta={'date': date},callback=self.parse)
    
    def parse(self, response):
        rows = response.xpath("//tbody//tr[.//td[contains(text(),'WIN ') or contains(text(),'IND ') or contains(text(),'DOL ') or contains(text(),'WDO ')]]")

        for row in rows:
            #print(row.extract())
            cells = row.xpath('.//td//text()').extract()
            line = [response.meta['date']] + [cell.strip() for cell in cells]
            print(line)


def date_range(start,end):

    start_date = parse(start)
    end_date = parse(end)
    
    date_list = list(rrule(freq=DAILY,dtstart=start_date,until=end_date,byweekday=(MO,TU,WE,TH,FR)))

    return [date.strftime("%d/%m/%Y") for date in date_list]