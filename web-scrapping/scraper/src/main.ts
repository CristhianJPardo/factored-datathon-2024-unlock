import { crawler } from './crawler.js'
import { logRunTime, loadSourceUrls } from './helpers.js'

const trunc = 100

const startTime = Date.now()

crawler.run([...loadSourceUrls(trunc)])
    .then(() => {
        logRunTime(startTime)
    })
    .catch(err => { throw err })
