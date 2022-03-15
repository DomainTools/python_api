from domaintools import API


dt_api = API(USER_NAME, KEY)

# Show currently monitored terms
result = dt_api.iris_detect_monitors().data()
print(result)

first_monitor_id = result['monitors'][0]['id']

# Show domains that match the term from the first monitor that are new
new_domains = dt_api.iris_detect_new_domains(first_monitor_id).data()
print(new_domains)

# Show domains that match the term from the first monitor that are currently watched
watched_domains = dt_api.iris_detect_watched_domains(first_monitor_id).data()
print(watched_domains)

first_new_domain_id = new_domains['watchlist_domains'][0]['id']
# Add a domain to the watched list
result = dt_api.iris_detect_manage_watchlist_domains(watchlist_domain_ids=[first_new_domain_id], state="watched")
print(result)

first_watched_domain_id = watched_domains['watchlist_domains'][0]['id']
# Add a domain to the blocked list
# Not going to actually run this, because you can't undo escalations
# result = dt_api.iris_detect_escalate_domains(watchlist_domain_ids=[first_watched_domain_id], escalation_type="blocked")