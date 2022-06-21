# SQL Heap Test

## Purpose

This repository is a simple demonstration of the computational impact of deleting and recreating clustered indexes in a
variety of situations.  The overall goal is to determine what a real effect is for dropping keys before inserts.

## Project Structure

Everything's in the root folder, as this is more for analysis than a dedicated project of sorts.  The files of importance are:

* `runTests.ipynb` - This is a Jupyter notebook that can be run to generate the `results_400000.pkl` and `results_1500000.pkl` files.
  * These also include the test cases, assumptions, and so on. 
* `results.ipynb` - This is a Jupyter notebook for the results of the tests, graphs, and outcomes.

## Assumptions and General Problem Statement/Hardware

There are 16 tests, looking at the performance impact of rebuilding both cluster and non-cluster indexes on a table given 
various scenarios.  The test results include a test number, description, classification, and time (in seconds) to completion.

The hardware this was run on is a Synology DiskStation with 32Gb of RAM and spin disks (no SSD) running QEMU.  In the QEMU
virtual machine we have SQL Server 2019 Developer, with 10Gb of RAM dedicated to the VM.

Best practices were used in the setup of SQL Server, including proper tempdb, max memory, DOP, etc.

## Research Inspiration

I have to thank the following article for the inspiration for this test:

[https://social.technet.microsoft.com/wiki/contents/articles/19211.dropping-a-clustered-index-will-not-reorganize-the-heap.aspx](https://social.technet.microsoft.com/wiki/contents/articles/19211.dropping-a-clustered-index-will-not-reorganize-the-heap.aspx)
