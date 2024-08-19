import { readFileSync } from "fs"

export const loadSourceUrls = (trunc = 0): string[] => {
    const fileName = 'source_urls.json'
    const data = readFileSync(fileName, 'utf-8')
    let sourceUrls: string[] = JSON.parse(data)
    if (trunc) {
        sourceUrls = sourceUrls.slice(0, trunc)
    }
    return sourceUrls
}

export const logRunTime = (startTime: number): void => {
    const timeTaken = Date.now() - startTime
    const days = Math.floor(timeTaken / (1000 * 60 * 60 * 24))
    const hours = Math.floor((timeTaken % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
    const minutes = Math.floor((timeTaken % (1000 * 60 * 60)) / (1000 * 60))
    const seconds = Math.floor((timeTaken % (1000 * 60)) / 1000)
    console.log(`Time taken: ${days}d ${hours}h ${minutes}m ${seconds}s`)
}

export const sanitizeTitle = (title: string): string => {
    return title.replace(/[\/\\?%*:|"<>]/g, '_').trim() + '.json'
}