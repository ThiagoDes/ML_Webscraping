import scrapy


class MlSpider(scrapy.Spider):
    name = 'ml'

    # start_urls = [f'https://www.mercadolivre.com.br/ofertas?page={page}' for page in range(1,210)]
    start_urls = [f'https://www.mercadolivre.com.br/ofertas?page=1']

    def parse(self, response, **kwarrgs):
        for item in response.xpath('//li[@class="promotion-item"]'):
            img = item.xpath('.//img/@src').get()
            promotion_price = item.xpath('.//span[@class="promotion-item__price"]//span//text()').getall()
            old_price = item.xpath('.//span[@class="promotion-item__oldprice"]//text()').getall()
            title = item.xpath('.//p[@class="promotion-item__title"]//text()').get()
            link = item.xpath('./a/@href').get()

            yield {
                'img' : img,
                'promotion_price' : promotion_price,
                'old_price' : old_price,
                'title' : title,
                'link' : link
            }
        
        next_page = response.xpath('//a[contains(@title, "Próxima")]/@href').get()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)
