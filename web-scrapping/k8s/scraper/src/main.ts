import { CheerioCrawler } from 'crawlee'
import { readFileSync } from 'fs'

function loadSourceUrls(): string[] {
    const fileName = 'source_urls.json'
    const data = readFileSync(fileName, 'utf-8')
    const sourceUrls: string[] = JSON.parse(data)
    return sourceUrls
}

const crawler = new CheerioCrawler({
    // Function called for each URL
    async requestHandler({ request, $, log }) {
        const title = $('title').text()
        log.info(`URL: ${request.url}\nTITLE: ${title}`)
    },
})


await crawler.run([...loadSourceUrls()])
