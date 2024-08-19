import { RequestHandler } from "crawlee"

export const requestHandler: RequestHandler = async ({ request, $, log }: any) => {
    const title = $('title').text()
    log.info(`URL: ${request.url}\nTITLE: ${title}`)
}