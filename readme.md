- `pip install kafka-python`
```
spark-submit \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.13:3.6.1 \
  consumer.py
```


```
# Start Zookeeper
bin/zookeeper-server-start.sh config/zookeeper.properties

# In a new terminal:
# Start Kafka broker
bin/kafka-server-start.sh config/server.properties

```

```
wget https://archive.apache.org/dist/kafka/3.6.1/kafka_2.13-3.6.1.tgz
tar -xvzf kafka_2.13-3.6.1.tgz
cd kafka_2.13-3.6.1
```
Great — let’s walk through **both** the Kafka setup and generating the `data.txt` file so you can run everything locally without issues.

---

## ✅ PART 1: Kafka & Zookeeper Setup (Local)

### 📦 Requirements:

* Java (8 or 11 recommended)
* Kafka 3.x (includes Zookeeper binaries)
* Python 3.x (for the producer)
* Apache Spark 3.x (for the consumer)

---

### 📥 Step 1: Download & Install Kafka

Download Kafka from:
👉 [https://kafka.apache.org/downloads](https://kafka.apache.org/downloads)

Or use `wget`:

```bash
wget https://archive.apache.org/dist/kafka/3.6.1/kafka_2.13-3.6.1.tgz
tar -xvzf kafka_2.13-3.6.1.tgz
cd kafka_2.13-3.6.1
```

---

### ▶️ Step 2: Start Zookeeper & Kafka

> Do this in **two separate terminals**.

**🖥 Terminal 1 — Start Zookeeper:**

```bash
bin/zookeeper-server-start.sh config/zookeeper.properties
```

**🖥 Terminal 2 — Start Kafka Broker:**

```bash
bin/kafka-server-start.sh config/server.properties
```

---

### ✅ Step 3: Create Kafka Topic

In another terminal:

```bash
bin/kafka-topics.sh --create --topic test-topic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

---

## ✅ PART 2: Generate `data.txt`

Let’s generate a sample file with 1000 records.

### 🔧 Python Script (to generate `data.txt`)

Create `generate_data.py`:

```python
with open('data.txt', 'w') as f:
    for i in range(1, 1001):
        f.write(f"record_{i}\n")

print("Generated data.txt with 1000 records.")
```

Run it:

```bash
python generate_data.py
```

This will create a file `data.txt` like:

```
record_1
record_2
...
record_1000
```

---

## ✅ PART 3: Final Command Summary

### ▶️ Terminal 1: Start Zookeeper

```bash
cd kafka_2.13-3.6.1
bin/zookeeper-server-start.sh config/zookeeper.properties
```

### ▶️ Terminal 2: Start Kafka Broker

```bash
cd kafka_2.13-3.6.1
bin/kafka-server-start.sh config/server.properties
```

### ▶️ Terminal 3: Create Topic (once)

```bash
cd kafka_2.13-3.6.1
bin/kafka-topics.sh --create --topic test-topic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

### ▶️ Terminal 4: Run Producer

```bash
python producer.py
```

### ▶️ Terminal 5: Run Spark Consumer

```bash
spark-submit \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0 \
  consumer.py
```

---


Thanks Gokul — you're almost there!

The error:

> `spark-submit: command not found`

...means **Apache Spark is not installed** or the `spark-submit` binary isn't on your system's PATH.

---

## ✅ Solution: Install Apache Spark

Let’s walk through **installing Spark** on your Ubuntu machine and getting `spark-submit` working.

---

### 🔧 Step 1: Install Prerequisites

You already have Java 17 — great.

Now install other essentials:

```bash
sudo apt update
sudo apt install wget unzip scala -y
```

---

### 📥 Step 2: Download Spark (Pre-built with Hadoop)

Recommended version: **Spark 3.4.1**

```bash
cd ~
wget https://downloads.apache.org/spark/spark-3.4.1/spark-3.4.1-bin-hadoop3.tgz
tar -xzf spark-3.4.1-bin-hadoop3.tgz
mv spark-3.4.1-bin-hadoop3 spark
```

---

### ⚙️ Step 3: Add Spark to Your PATH

Edit your shell config (`~/.bashrc` or `~/.zshrc`, depending on your shell):

```bash
nano ~/.bashrc
```

Add these lines at the bottom:

```bash
export SPARK_HOME=~/spark
export PATH=$SPARK_HOME/bin:$PATH
```

Then apply the changes:

```bash
source ~/.bashrc
```

---

### ✅ Step 4: Verify

Now check if `spark-submit` works:

```bash
spark-submit --version
```

Expected output:

```
Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /___/ .__/\_,_/_/ /_/\_\   version 3.4.1
      /_/
```

---

### ✅ Step 5: Run Your Consumer

Now you can run your consumer like this:

```bash
spark-submit \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0 \
  consumer.py
```

---

Let me know once you've got Spark installed and working — then we can test your consumer! Or I can help verify your full setup.

Thanks, Gokul — this confirms the issue 🔍:

> Inside `~/spark/`, you still have a subfolder called `spark-3.4.1-bin-hadoop3`, meaning the Spark binary isn't at `~/spark/bin`, but at `~/spark/spark-3.4.1-bin-hadoop3/bin`.

---

## ✅ Here's What You Need to Do:

Thanks for the details, Gokul — here’s what’s happening:

---

## ⚠️ Problem Recap

You're still seeing:
```
Failed to find Spark jars directory (/home/gokul_articence/spark/assembly/target/scala-2.12/jars)
You need to build Spark with the target "package" before running this program.
```

This only happens when you’re **accidentally inside Spark source code**, not the **prebuilt Spark binary**.

---

## ✅ Let's Fix It — Clean and Correct Steps

Here’s the **definitive fix**:

---

### 🔁 1. Remove broken Spark directory (optional, for cleanup)

Just to avoid confusion:

```bash
rm -rf ~/spark
```

---

### 📥 2. Download Correct Prebuilt Spark Binary

```bash
cd ~
wget https://archive.apache.org/dist/spark/spark-3.4.1/spark-3.4.1-bin-hadoop3.tgz
tar -xzf spark-3.4.1-bin-hadoop3.tgz
mv spark-3.4.1-bin-hadoop3 spark
```

✅ Now, `~/spark/bin/spark-submit` **must exist**

---

### ⚙️ 3. Set Environment Variables

Edit `.bashrc`:

```bash
nano ~/.bashrc
```

At the bottom, ensure you have:

```bash
export SPARK_HOME=~/spark
export PATH=$SPARK_HOME/bin:$PATH
```

Then apply:

```bash
source ~/.bashrc
```

---

### ✅ 4. Test

```bash
spark-submit --version
```

✅ Expected output:

```
Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /___/ .__/\_,_/_/ /_/\_\   version 3.4.1
      /_/
```

---

Once this works, you're 100% ready to run:

```bash
spark-submit \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0 \
  consumer.py
```

Let me know when you see the Spark banner!


### 🔁 Step 1: Move the actual Spark binary up

You're in the wrong directory level. Fix this by running:

```bash
cd ~
rm -rf spark  # remove the wrongly-structured folder
mv spark-3.4.1-bin-hadoop3 spark  # correctly rename the extracted folder
```

Now, `~/spark/bin/spark-submit` will exist as expected.

---

### ✅ Step 2: Re-export paths

Update your environment:

```bash
export SPARK_HOME=~/spark
export PATH=$SPARK_HOME/bin:$PATH
source ~/.bashrc
```

You can optionally add those lines to `~/.bashrc` permanently if not already there.

---

### ✅ Step 3: Verify Again

Now test:

```bash
spark-submit --version
```

✅ You should finally see:

```
Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /___/ .__/\_,_/_/ /_/\_\   version 3.4.1
      /_/
```

---

### 🎯 Final Note

Let me know if you'd like to **run the Spark Kafka consumer now** — we can move forward from here once `spark-submit` works correctly.
