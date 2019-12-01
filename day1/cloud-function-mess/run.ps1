
$content = get-content "input"

$data = $content -join ";"

write-host $data

gcloud pubsub topics publish aoc_2019_1_input --message $data
