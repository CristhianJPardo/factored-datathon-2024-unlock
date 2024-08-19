import { CheerioCrawler } from 'crawlee'
import path from 'path'
import { sanitizeTitle } from './helpers'
import { existsSync, mkdirSync, writeFileSync } from 'fs'


export const crawler = new CheerioCrawler({
    async requestHandler({ request, $ }) {
        const title = $('title').text()
        const paragraphs = $('p').map((i, el) => $(el).text()).get()

        const data = {
            title: title,
            content: paragraphs
        }
        const fileName = sanitizeTitle(title)
        const directory = 'extraction'
        const filePath = path.join(directory, fileName)

        if (!existsSync(directory)) {
            mkdirSync(directory, { recursive: true })
        }

        writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf-8')

        console.log(`Data written to ${filePath}`)

    },

    // async requestHandler({ request, $, log }) {
    //     const title = $('title').text()
    //     log.info(`URL: ${request.url}\nTITLE: ${title}`)
    // },
})