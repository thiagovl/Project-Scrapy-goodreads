import scrapy
from scrapy.loader import ItemLoader
from demo_project.items import QuoteItem # A classe criada

# Criando a classe, ela deve herdar da classe scrapy - scrapy.Spider
class GoodReadsSpider(scrapy.Spider):
    # Divisões da Spider: identity, request, response

    # identity - nome da Spider
    name = 'goodreads'

    # request - requisiçoes
    # def start_requests(self):
        # Endereço de pesquisa
    #    url = 'https://www.goodreads.com/quotes?page=1'

    #    yield scrapy.Request(url=url, callback=self.parse) # callback será responsável por capturar as respostas e passar para a função parse

    # Forma resumida de start_request
    start_urls = [
        'https://www.goodreads.com/quotes?page=1'
    ]

    # response - obtém a resposta da URL pesquisada acima
    def parse(self, response):

        # Forma resumida de response.selector.xpath é response.xpath
        for quote in response.xpath("//div[@class='quote']"): # Percorre a resposta em busca da div com a class quote

            # Importando a classe QuoteItem do arquivo items.py para limpar os dados
            loader = ItemLoader(item=QuoteItem(), selector=quote, response=response)
            loader.add_xpath('text', ".//div[@class='quoteText']/text()[1]")
            loader.add_xpath('author', ".//div[@class='quoteText']/child::span")
            loader.add_xpath('tags', ".//div[@class='greyText smallText left']/a")
            # Carregando o objeto
            yield loader.load_item()
            
            # Pegando o link da próxima página dinamicamente e fazendo scrapy
            next_page = response.xpath("//a[@class='next_page']/@href").extract_first() # Busca o link a da próxima página na tag a
            if next_page is not None:
                next_page_link = response.urljoin(next_page) # Pega o link da próxima página
                yield scrapy.Request(url=next_page_link, callback=self.parse)
