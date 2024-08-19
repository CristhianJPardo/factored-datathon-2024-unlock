import { CheerioCrawler } from 'crawlee'


export const crawler = new CheerioCrawler({
    async requestHandler({ request, $, log }) {
        const title = $('title').text()
        log.info(`URL: ${request.url}\nTITLE: ${title}`)
    },
})