import pandas as pd
def main(repo_name):
    users_dict={"ceph":['batrick','cbodley','dillaman','dzafman','jcsp','liewegas','majianpeng'],
    "pytorch":['jamesr66a','jerryzh168','malfet','mrshenli','peterjc123','rohan-varma','seemethere'],
    "swift":['DougGregor','aschwaighofer','compnerd','dan-zheng','eeckstein','gottesmm','jckarter']
    }
    csv_file = "ceph_diff.csv"
    csv_data = pd.read_csv(f"{repo_name}", low_memory = False)
    csv_df = pd.DataFrame(csv_data)

if __name__=="__main__":
    repo_names=["ceph","pytorch","swift"]
    for repo_name in repo_names:
        main(repo_name)
    
