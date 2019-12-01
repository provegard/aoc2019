call gcloud functions deploy calc_fuel --runtime python37 --trigger-topic aoc_2019_1_mass --allow-unauthenticated

call gcloud functions deploy parse_input --runtime python37 --trigger-topic aoc_2019_1_input --allow-unauthenticated

call gcloud functions deploy aggregate --runtime python37 --trigger-topic aoc_2019_1_agg --allow-unauthenticated