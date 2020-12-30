import subprocess
import sys

# нам найти разницу между веткой и апстримом и отсечь те, коммиты, которые мы уже перенесли; делаем это в три шага:

# сначала получаем все потенциально новые коммиты - те, которыми отличается наша ветка и upstream/master для данного пути, 
# отсекаем часть коммитов через опцию --cherry

# потом получаем все коммиты в нашей ветке до общей базы с апстримом
# далее высчитываем для всех коммитов их patch id

# далее сверяем patch id, все коммиты из потенциально новых, для которых нет коммитов в нашей ветке с тем же patch id
# являются искомой разницей между ветками

def calc_id(commit_hash):
    cmd = ['git', 'log', '-1', '-p', commit_hash]
    diff = subprocess.check_output(cmd)
    cmd = ['git', 'patch-id']
    git = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, _ = git.communicate(input=diff, timeout=15)
    res = out.decode('utf-8').replace('\n','').split(' ')
    print("calc_id, hash: %s" % commit_hash)
    print("res: ")
    print(repr(res))
    return res


branch = sys.argv[1]
path = sys.argv[2]
cp = sys.argv[3]

cmd = ["git", "log", '--pretty=format:"%H"', '--cherry', '%s..upstream/master' % branch, "%s" % path]
commits_str = subprocess.check_output(cmd)

commits = commits_str.decode('utf-8').replace('"','').split('\n')
print(repr(commits))

base = subprocess.check_output(['git', 'merge-base', branch, 'upstream/master']).decode('utf-8').replace('"','').replace('\n','')
print('base')
print(repr(base))
branch_commits = subprocess.check_output(["git", "log", '--pretty=format:"%H"', '--cherry', '%s..%s' % (base, branch), "%s" % path]).decode('utf-8').replace('"','').split('\n')
print('bcommits')
print(repr(branch_commits))

new_commits = commits
to_remove = []

if len(branch_commits) >1 or branch_commits[0] != '':
    ids = []
    for commit in commits:
        ids.append(calc_id(commit))
    print('ids')
    print(repr(ids))

    branch_ids = []
    for branch_commit in branch_commits:
        branch_ids.append(calc_id(branch_commit))
    print('bids')
    print(repr(branch_ids))

    id_key = lambda id: id[0]
    sorted_ids = sorted(ids, key=id_key)
    sorted_branch_ids = sorted(branch_ids, key=id_key)

    i = 0
    j = 0
    ids_len = len(sorted_ids)
    branch_len = len(sorted_branch_ids)
    while (i < ids_len) and (j < branch_len):
        if sorted_branch_ids[j][0] < sorted_ids[i][0]:
            j = j + 1
        elif sorted_branch_ids[j][0] > sorted_ids[i][0]:
            i = i + 1
        else:
            to_remove.append(sorted_ids[i][1])
            i = i + 1
            j = j + 1

if to_remove:
    for v in to_remove:
        i = new_commits.index(v)
        del new_commits[i]

print('new_commits')
print(new_commits)

for c in new_commits:
    subprocess.call(['git', 'log', '-1', '--oneline', c])

if cp == '--cherry-pick':
    cmd = ['git', 'cherry-pick']
    for v in reversed(new_commits):
        cmd.append(v)
    print(repr(cmd))
    subprocess.call(cmd)