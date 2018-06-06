## How-to:

This folder should imperatively contain both:
- `full_omop_login.npy`, containing your credentials to the OMOP database ;
- `userconfig.yml`, containing all the paths we wish to automatically import when loading file `fleming_lib/paths.py`.

Example of `userconfig.yml`:

```yaml
USERPATHS:
  FLEMING:  '/home/paulroujansky/git/DataForGood/batch4_diafoirus_fleming'
```
