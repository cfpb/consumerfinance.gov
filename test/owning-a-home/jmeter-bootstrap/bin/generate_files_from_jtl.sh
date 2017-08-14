#usage: ./generate_files_from_jtl.sh [file-prefix]
#example: ./generate_files_from_jtl.sh my_test
# See http://jmeter-plugins.org/wiki/JMeterPluginsCMD/ for documentation

cmd="java -jar apache-jmeter-2.11/lib/ext/CMDRunner.jar --tool Reporter --input-jtl results/$1.jtl"

png="$cmd --generate-png"
$cmd --generate-csv results/$1_aggregate-report.csv --plugin-type AggregateReport
$png results/$1_bytes-throughput-over-time.png --plugin-type BytesThroughputOverTime
$png results/$1_hits-per-second.png --plugin-type HitsPerSecond
$png results/$1_latencies-over-time.png --plugin-type LatenciesOverTime
$png results/$1_response-times-distribution.png --plugin-type ResponseTimesDistribution
$png results/$1_response-times-percentiles.png --plugin-type ResponseTimesPercentiles
$png results/$1_throughput-vs-threads.png --plugin-type ThroughputVsThreads
$png results/$1_response-codes-per-second.png --plugin-type ResponseCodesPerSecond
$png results/$1_transactions-per-second.png --plugin-type TransactionsPerSecond
