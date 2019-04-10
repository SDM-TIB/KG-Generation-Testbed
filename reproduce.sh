#!/bin/bash

# Generate Data
echo "Generating Data ... "
python3 data-generator/generate_data.py

echo "Join selectivity"

declare -a array=("1k_rows" "3k_rows" "10k_rows" "50k_rows")
declare -a percents=("5_percent" "10_percent"  "20_percent" "30_percent" "50_percent")
declare -a lowpercents=("60_percent" "80_percent" "100_percent")
#declare -a relationType=("one-one" "one-N")
#declare -a percents=("10_25" "10_50" "5_25" "5_50" "15_25" "15_50")

for j in "${array[@]}"
do
	for i in "${percents[@]}"
	do
		echo "Running $j - $i"
		#table1
		cp data/joinselectivity/high_selectivity/$j/table1.csv data/table1.csv
		#table2
		cp data/joinselectivity/high_selectivity/$j/table2_$i.csv data/table2.csv

		start=$(date +%s.%N)
		python3 tools/rdfizer-master/rdfizer/run_rdfizer.py mappings/config.ini
		dur=$(echo "$(date +%s.%N) - $start" | bc)

		noutput=$(wc -l results/result-1.nt | cut -d " " -f 1)
		first=$(sed '2q;d' results/result_datasets_stats.csv | cut -d "," -f 3)
		

		echo "rdfizer,$j,$i,$dur,$first,$noutput"  >> results/results-selectivity.csv
		mv results/result_datasets_stats.csv results/continuos/selectivity-$j-$i.csv
		rm results/result-1.nt

		start=$(date +%s.%N)
		java -jar tools/rmlmapper.jar -m mappings/mapping.rml.ttl -o output.nt -d
		dur=$(echo "$(date +%s.%N) - $start" | bc)
		
		noutput=$(wc -l output.nt | cut -d " " -f 1)
		echo "rmlmapper,$j,$i,$dur,$dur,$noutput"  >> results/results-selectivity.csv

		rm output.nt
		rm data/table1.csv
		rm data/table2.csv
	done
done

for j in "${arrJoinSelectivity[@]}"
do
	for i in "${percents[@]}"
	do
		#table1
		echo "Running $j - $i"
		cp data/low_selectivity/$j/table1.csv data/table1.csv
		#table2
		cp data/low_selectivity/$j/table2_$i.csv data/table2.csv

		start=$(date +%s.%N)
		python3 tools/rdfizer-master/rdfizer/run_rdfizer.py mappings/config.ini
		dur=$(echo "$(date +%s.%N) - $start" | bc)

		first=$(sed '2q;d' results/result_datasets_stats.csv | cut -d ","  -f 3)
		noutput=$(wc -l results/result-1.nt | cut -d " " -f 1)

		echo "rdfizer,$j,$i,$dur,$first,$noutput"  >> results/results-selectivity.csv
		mv results/result_datasets_stats.csv results/continuos/select-low-$j-$i.csv
		rm results/result-1.nt

		start=$(date +%s.%N)
		java -jar tools/rmlmapper.jar -m mappings/mapping.rml.ttl -o output.nt -d
		dur=$(echo "$(date +%s.%N) - $start" | bc)

		noutput=$(wc -l output.nt | cut -d " " -f 1)
		echo "rmlmapper,$j,$i,$dur,$dur,$noutput"  >> results/results-selectivity.csv

		rm output.nt
		rm data/table1.csv
		rm data/table2.csv
	done
done

echo "One-to-N and N-to-One ... "

declare -a arrJoinSelectivity=("1k_rows" "3k_rows" "10k_rows" "50k_rows")
declare -a percents=("50_10_50_percent" "50_15_50_percent" "50_5_50_percent" "50_10_25_percent" "50_15_25_percent" "50_5_25_percent")

for j in "${arrJoinSelectivity[@]}"
do
	for i in "${percents[@]}"
	do
		echo "Running one-to-n $j - $i"
		#table1
		cp data/relation_type/$t/$j/table1.csv data/table1.csv
		#table2
		cp data/relation_type/$t/$j/table2_$i.csv data/table2.csv

		start=$(date +%s.%N)
		python3 tools/rdfizer-master/rdfizer/run_rdfizer.py mappings/config.ini
		dur=$(echo "$(date +%s.%N) - $start" | bc)

		noutput=$(wc -l results/result-1.nt | cut -d " " -f 1)
		first=$(sed '2q;d' results/result_datasets_stats.csv | cut -d "," -f 3)
	

		echo "rdfizer,one-n,$j,$i,$dur,$first,$noutput"  >> results/results-join-type.csv
		mv results/result_datasets_stats.csv results/continuos/join-type-$j-$i-one-n.csv
		rm results/result-1.nt

		start=$(date +%s.%N)
		java -jar tools/rmlmapper.jar -m mappings/mapping.rml.ttl -o output.nt -d
		dur=$(echo "$(date +%s.%N) - $start" | bc)
		
		noutput=$(wc -l output.nt | cut -d " " -f 1)
		echo "rmlmapper,one-n,$j,$i,$dur,$dur,$noutput"  >> results/results-join-type.csv

		rm output.nt
			
		mv data/table1.csv data/table22.csv
		mv data/table2.csv data/table1.csv
		mv data/table22.csv data/table2.csv	
		echo "Running n-to-one $j - $i"

		start=$(date +%s.%N)
		python3 tools/rdfizer-master/rdfizer/run_rdfizer.py mappings/config.ini
		dur=$(echo "$(date +%s.%N) - $start" | bc)

		noutput=$(wc -l results/result-1.nt | cut -d " " -f 1)
		first=$(sed '2q;d' results/result_datasets_stats.csv | cut -d "," -f 3)
	

		echo "rdfizer,n-one,$j,$i,$dur,$first,$noutput"  >> results/results-join-type.csv
		mv results/result_datasets_stats.csv results/continuos/join-type-$j-$i-n-one.csv
		rm results/result-1.nt

		start=$(date +%s.%N)
		java -jar tools/rmlmapper.jar -m mappings/mapping.rml.ttl -o output.nt -d
		dur=$(echo "$(date +%s.%N) - $start" | bc)
		
		noutput=$(wc -l output.nt | cut -d " " -f 1)
		echo "rmlmapper,n-one,$j,$i,$dur,$dur,$noutput"  >> results/results-join-type.csv


		rm output.nt
		rm data/table1.csv
		rm data/table2.csv
		

	done
done
echo "N-to-M ..."

mv mappings/mapping.rml.ttl mappings/mapping3.rml.ttl
mv mappings/mapping_n_m.rml.ttl mappings/mapping.rml.ttl

declare -a array=("1k_rows" "3k_rows" "10k_rows" "50k_rows")
declare -a percents=("50_10_10_10_percent" "50_10_5_25_percent" "50_3_3_50_percent" "50_5_3_10_percent" "50_10_10_25_percent" "50_10_5_50_percent" "50_3_5_10_percent" "50_5_3_25_percent" "50_10_10_50_percent" "50_3_10_10_percent" "50_3_5_25_percent" "50_5_3_50_percent" "50_10_3_10_percent" "50_3_10_25_percent" "50_3_5_50_percent" "50_5_5_10_percent" "50_10_3_25_percent" "50_3_10_50_percent" "50_5_10_10_percent" "50_5_5_25_percent" "50_10_3_50_percent" "50_3_3_10_percent" "50_5_10_25_percent" "50_5_5_50_percent" "50_10_5_10_percent" "50_3_3_25_percent" "50_5_10_50_percent")

for j in "${array[@]}"
do
	for i in "${percents[@]}"
	do
		echo "Running n-to-m $j - $i"
		#table1
		cp data/relation_type/N-M/$j/table1_$i.csv data/table1.csv
		#table2
		cp data/relation_type/N-M/$j/table2_$i.csv data/table2.csv

		start=$(date +%s.%N)
		python3 tools/rdfizer-master/rdfizer/run_rdfizer.py mappings/config.ini
		dur=$(echo "$(date +%s.%N) - $start" | bc)

		noutput=$(wc -l results/result-1.nt | cut -d " " -f 1)
		first=$(sed '2q;d' results/result_datasets_stats.csv | cut -d "," -f 3)
	
		echo "rdfizer,n-m,$j,$i,$dur,$first,output"  >> results/results-join-type.csv
		mv results/result_datasets_stats.csv results/continuos/join-type-$j-$i.csv
		rm results/result-1.nt

		start=$(date +%s.%N)
		java -jar tools/rmlmapper.jar -m mappings/mapping.rml.ttl -o output.nt -d
		dur=$(echo "$(date +%s.%N) - $start" | bc)
		
		noutput=$(wc -l output.nt | cut -d " " -f 1)
		echo "rmlmapper,n-m,$j,$i,$dur,$dur,$noutput"  >> results/results-join-type.csv

		rm output.nt
		rm data/table1.csv
		rm data/table2.csv
	done
done

mv mappings/mapping.rml.ttl mappings/mapping_n_m.rml.ttl
mv mappings/mapping3.rml.ttl mappings/mapping.rml.ttl
echo "Duplicates on join ..."

declare -a array=("1k_rows" "3k_rows" "10k_rows" "50k_rows")
declare -a percents=("10_10_percent" "10_20_percent" "10_30_percent" "10_40_percent" "10_50_percent" "10_5_percent" "20_10_percent" "20_20_percent" "20_30_percent" "20_40_percent" "20_50_percent" "20_5_percent" "3_10_percent" "3_20_percent" "3_30_percent" "3_40_percent" "3_50_percent" "3_5_percent" "5_10_percent" "5_20_percent" "5_30_percent" "5_40_percent" "5_50_percent" "5_5_percent")
	
for j in "${array[@]}"
do
	for i in "${percents[@]}"
	do
		echo "Running duplicates $j - $i"
		#table1
		cp data/JoinDuplicates/$j/table1.csv data/table1.csv
		#table2
		cp data/JoinDuplicates/$j/table2_$i.csv data/table2.csv

		start=$(date +%s.%N)
		python3 tools/rdfizer-master/rdfizer/run_rdfizer.py mappings/config.ini
		dur=$(echo "$(date +%s.%N) - $start" | bc)

		noutput=$(wc -l results/result-1.nt | cut -d " " -f 1)
		first=$(sed '2q;d' results/result_datasets_stats.csv | cut -d "," -f 3)
	
		echo "rdfizer,$j,$i,$dur,$first,$noutput"  >> results/results-duplicates.csv
		mv results/result_datasets_stats.csv results/continuos/duplicates-$j-$i.csv
		rm results/result-1.nt

		start=$(date +%s.%N)
		java -jar tools/rmlmapper.jar -m mappings/mapping.rml.ttl -o output.nt -d
		dur=$(echo "$(date +%s.%N) - $start" | bc)
		
		noutput=$(wc -l output.nt | cut -d " " -f 1)
		echo "rmlmapper,$j,$i,$dur,$dur,$noutput"  >> results/results-duplicates.csv

		rm output.nt
		rm data/table1.csv
		rm data/table2.csv
	done
done

echo "Navie - Different dataset sizes"

declare -a arrJoinSelectivity=("1k_rows" "3k_rows" "10k_rows" "50k_rows")
declare -a percents=("10_columns_table" "20_columns_table" "2_columns_table" "30_columns_table" "5_columns_table")
mv mappings/mapping.rml.ttl mappings/mapping2.rml.ttl
for j in "${arrJoinSelectivity[@]}"
do
	for i in "${percents[@]}"
	do
		mv mappings/$i.rml.ttl mappings/mapping.rml.ttl
		#table1
		echo "Running $j - $i"
		cp data/naive/$j/$i.csv data/table.csv
		#table2

		start=$(date +%s.%N)
		python3 tools/rdfizer-master/rdfizer/run_rdfizer.py mappings/config.ini
		dur=$(echo "$(date +%s.%N) - $start" | bc)

		first=$(sed '2q;d' results/result_datasets_stats.csv | cut -d ","  -f 3)
		noutput=$(wc -l results/result-1.nt | cut -d " " -f 1)

		echo "rdfizer,$j,$i,$dur,$first"  >> results/results-naive.csv
		mv results/result_datasets_stats.csv results/continuos/join-naive-$j-$i.csv
		rm results/result-1.nt

		start=$(date +%s.%N)
		java -jar tools/rmlmapper.jar -m mappings/mapping.rml.ttl -o output.nt -d
		dur=$(echo "$(date +%s.%N) - $start" | bc)

		noutput=$(wc -l output.nt | cut -d " " -f 1)
		echo "rmlmapper,$j,$i,$dur,$dur,$noutput"  >> results/results-naive.csv
		mv mappings/mapping.rml.ttl mappings/$i.rml.ttl
		rm output.nt
		rm data/table.csv
	done
done
mv mappings/mapping2.rml.ttl mappings/mapping.rml.ttl

